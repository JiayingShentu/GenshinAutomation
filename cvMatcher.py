import cv2 as cv
import numpy as np

def showKeyPoints(img, keyPoints):
    imgWithKeyPoints = cv.drawKeypoints(img, keyPoints, img, color=(255, 0, 255))
    cv.imshow('Key Points', imgWithKeyPoints)
    cv.waitKey(0)

def match(fileName, capture):
    pattern = cv.imread(fileName, 0)
    sift = cv.SIFT_create(1000)
    capture = cv.cvtColor(capture, cv.COLOR_BGRA2GRAY)
    patternKeyPoints, patternDescriptor = sift.detectAndCompute(pattern, None)
    captureKeyPoints, captureDescriptor = sift.detectAndCompute(capture, None)
    
    #showKeyPoints(capture, captureKeyPoints)
    #showKeyPoints(pattern, patternKeyPoints)
    
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(patternDescriptor, captureDescriptor, 2)

    ratio_thresh = 0.7
    good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)
    
    img_matches = np.empty((max(pattern.shape[0], capture.shape[0]), pattern.shape[1]+capture.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(pattern, patternKeyPoints, capture, captureKeyPoints, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    #cv.imshow('Good Matches', img_matches)
    #cv.waitKey()

    match_threshold = 3
    if len(good_matches) < match_threshold:
        print("cvMatcher: match failed.")
        return None
    print("cvMatcher: match succeeded.")

    sceneX = []
    sceneY = []
    for i in range(len(good_matches)):
        sceneX.append(captureKeyPoints[good_matches[i].trainIdx].pt[0])
        sceneY.append(captureKeyPoints[good_matches[i].trainIdx].pt[1])
    # cv.imshow('Good Matches & Object detection', img_matches)
    # cv.waitKey()
    return [sorted(sceneX)[len(sceneX) // 2], sorted(sceneY)[len(sceneY) // 2]]
    # left, top, right, bottom = min(sceneX), min(sceneY), max(sceneX), max(sceneY)
    
    # cv.line(img_matches, (int(left + pattern.shape[1]), int(top)),\
    # (int(right + pattern.shape[1]), int(top)), (0,255,0), 4)
    # cv.line(img_matches, (int(right + pattern.shape[1]), int(top)),\
    # (int(right + pattern.shape[1]), int(bottom)), (0,255,0), 4)
    # cv.line(img_matches, (int(right + pattern.shape[1]), int(bottom)),\
    # (int(left + pattern.shape[1]), int(bottom)), (0,255,0), 4)
    # cv.line(img_matches, (int(left + pattern.shape[1]), int(bottom)),\
    # (int(left + pattern.shape[1]), int(top)), (0,255,0), 4)
        
    # cv.imshow('Good Matches & Object detection', img_matches)
    # cv.waitKey()
    # return [left, top, right, bottom]