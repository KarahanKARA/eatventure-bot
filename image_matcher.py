import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ImageMatcher:
    def __init__(self, threshold=0.85):
        self.threshold = threshold
    
    def load_template(self, template_path):
        template = cv2.imread(str(template_path), cv2.IMREAD_UNCHANGED)
        if template is None:
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        mask = None
        if len(template.shape) == 3 and template.shape[2] == 4:
            alpha = template[:, :, 3]
            mask = np.zeros_like(alpha)
            mask[alpha > 0] = 255
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
        return template, mask
    
    def find_template(self, screenshot, template, mask=None, threshold=None, template_name="Unknown", check_color=False):
        thresh = threshold if threshold else self.threshold
        
        if template.shape[0] > screenshot.shape[0] or template.shape[1] > screenshot.shape[1]:
            logger.debug(f"Template is larger than screenshot. Template: {template.shape}, Screenshot: {screenshot.shape}")
            return False, 0.0, 0, 0
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED, mask=mask)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        confidence = 1 - min_val
        
        if confidence >= thresh:
            h, w = template.shape[:2]
            center_x = min_loc[0] + w // 2
            center_y = min_loc[1] + h // 2
            
            if check_color:
                color_match = self._check_color_similarity(screenshot, template, min_loc, mask)
                if not color_match:
                    logger.debug(f"[{template_name}] Color check failed at ({center_x}, {center_y}), confidence: {confidence:.2%}")
                    return False, confidence, 0, 0
            
            logger.debug(f"[{template_name}] Found at ({center_x}, {center_y}), confidence: {confidence:.2%}")
            return True, confidence, center_x, center_y
        
        return False, confidence, 0, 0
    
    def _check_color_similarity(self, screenshot, template, location, mask=None):
        x, y = location
        h, w = template.shape[:2]
        
        roi = screenshot[y:y+h, x:x+w]
        
        if roi.shape[:2] != template.shape[:2]:
            return True
        
        if mask is not None:
            template_masked = cv2.bitwise_and(template, template, mask=mask)
            roi_masked = cv2.bitwise_and(roi, roi, mask=mask)
        else:
            template_masked = template
            roi_masked = roi
        
        hist_template_b = cv2.calcHist([template_masked], [0], mask, [32], [0, 256])
        hist_template_g = cv2.calcHist([template_masked], [1], mask, [32], [0, 256])
        hist_template_r = cv2.calcHist([template_masked], [2], mask, [32], [0, 256])
        
        hist_roi_b = cv2.calcHist([roi_masked], [0], mask, [32], [0, 256])
        hist_roi_g = cv2.calcHist([roi_masked], [1], mask, [32], [0, 256])
        hist_roi_r = cv2.calcHist([roi_masked], [2], mask, [32], [0, 256])
        
        cv2.normalize(hist_template_b, hist_template_b, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_template_g, hist_template_g, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_template_r, hist_template_r, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_roi_b, hist_roi_b, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_roi_g, hist_roi_g, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_roi_r, hist_roi_r, 0, 1, cv2.NORM_MINMAX)
        
        corr_b = cv2.compareHist(hist_template_b, hist_roi_b, cv2.HISTCMP_CORREL)
        corr_g = cv2.compareHist(hist_template_g, hist_roi_g, cv2.HISTCMP_CORREL)
        corr_r = cv2.compareHist(hist_template_r, hist_roi_r, cv2.HISTCMP_CORREL)
        
        avg_corr = (corr_b + corr_g + corr_r) / 3
        
        color_threshold = 0.7
        return avg_corr >= color_threshold
    
    def find_all_templates(self, screenshot, template, mask=None, threshold=None, min_distance=15, scales=None, template_name="Unknown"):
        thresh = threshold if threshold else self.threshold
        all_matches = []
        
        if scales is None:
            scales = [1.0]
        
        if template.shape[0] > screenshot.shape[0] or template.shape[1] > screenshot.shape[1]:
            logger.debug(f"Template is larger than screenshot. Template: {template.shape}, Screenshot: {screenshot.shape}")
            return []
        
        for scale in scales:
            if scale != 1.0:
                scaled_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                scaled_mask = None
                if mask is not None:
                    scaled_mask = cv2.resize(mask, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                    scaled_mask[scaled_mask > 0] = 255
            else:
                scaled_template = template
                scaled_mask = mask
            
            if scaled_template.shape[0] > screenshot.shape[0] or scaled_template.shape[1] > screenshot.shape[1]:
                continue
            
            result = cv2.matchTemplate(screenshot, scaled_template, cv2.TM_SQDIFF_NORMED, mask=scaled_mask)
            
            locations = np.where(result <= (1 - thresh))
            
            h, w = scaled_template.shape[:2]
            for pt in zip(*locations[::-1]):
                confidence = 1 - result[pt[1], pt[0]]
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                logger.debug(f"[{template_name}] Found at ({center_x}, {center_y}), confidence: {confidence:.2%}")
                all_matches.append((confidence, center_x, center_y, w, h))
        
        if all_matches:
            all_matches = self._non_max_suppression(all_matches, min_distance)
        
        return [(conf, x, y) for conf, x, y, _, _ in all_matches]
    
    def _non_max_suppression(self, matches, min_distance):
        if not matches:
            return []
        
        matches = sorted(matches, key=lambda x: x[0], reverse=True)
        filtered = []
        
        for conf, x, y, w, h in matches:
            is_unique = True
            for f_conf, fx, fy, fw, fh in filtered:
                dx = abs(x - fx)
                dy = abs(y - fy)
                
                if dx < min_distance and dy < min_distance:
                    x1, y1 = max(x - w//2, fx - fw//2), max(y - h//2, fy - fh//2)
                    x2, y2 = min(x + w//2, fx + fw//2), min(y + h//2, fy + fh//2)
                    
                    if x2 > x1 and y2 > y1:
                        intersection = (x2 - x1) * (y2 - y1)
                        area1 = w * h
                        area2 = fw * fh
                        union = area1 + area2 - intersection
                        iou = intersection / union if union > 0 else 0
                        
                        if iou > 0.1:
                            is_unique = False
                            break
            
            if is_unique:
                filtered.append((conf, x, y, w, h))
        
        return filtered
