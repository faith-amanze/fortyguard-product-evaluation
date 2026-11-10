# FortyGuard Product Evaluation Report

**Project:** FortyGuard Temperature Dashboard and API  
**Prepared by:** Faith Amanze  
**Date:** 10 November 2026

## 1. Executive Summary

This evaluation examined the FortyGuard Temperature Dashboard and API to assess their functionality, analytical capabilities, response handling, and visualization features.

The evaluation covered four main analytical functions:

- Temperature Classification Map (TCM)
- Time of Measure
- Exceedance
- Persistence

Python scripts were used to submit API requests, retrieve results, inspect JSON responses, compare outputs, and generate a heatmap visualization.

The tested analytical requests completed successfully, although some limitations were observed around geographical coverage, response times, and the interpretation of certain environmental measurements.

## 2. Objectives

The objectives were to:

1. Test the main analytical API endpoints.
2. Verify that submitted requests return completed results.
3. Inspect the structure and consistency of API responses.
4. Evaluate geographical coverage and error handling.
5. Examine dashboard visualization and environmental data.
6. Identify limitations and opportunities for improvement.

## 3. Tools and Technologies

- Python
- Requests
- JSON
- Git and GitHub
- FortyGuard API
- Matplotlib for heatmap visualization

## 4. API Evaluation

### 4.1 Temperature Classification Map (TCM)

The TCM endpoint was tested using a Colorado geographical polygon.

**Observed results:**
- HTTP response: 200 OK
- Analysis status: Completed
- Number of tile features: 90
- Minimum temperature: 35.3936°C
- Maximum temperature: 35.6786°C
- Mean temperature: 35.5619°C
- Standard deviation: 0.0441°C

A histogram was also returned, with frequencies of 82 and 8 across the two reported temperature bins.

A separate request using a New York polygon returned HTTP 400 with an `OUT_OF_COVERAGE` error.

**Finding:** The endpoint successfully processed the Colorado request. However, geographical coverage is restricted; support for one US region does not guarantee support for all US locations.

### 4.2 Time of Measure

Two requests were submitted for July 15, 2024, using Colorado local time.

| Requested local time | Returned UTC window | Tile value |
|---|---|---:|
| 14:00 | 20:00 UTC | 20 |
| 15:00 | 21:00 UTC | 21 |

Both requests returned 90 tile values.

**Finding:** The returned UTC windows were consistent with the expected six-hour conversion from Colorado local time during July. The result also indicated a nearest-catalog-cell representation.

### 4.3 Exceedance

The Exceedance endpoint was tested using:

- Filter type: 2 (hour range)
- Time range: 14:00–16:00
- Threshold: 30°C
- Condition: Above threshold
- Resolution: 100 metres

**Observed results:**
- HTTP response: 200 OK
- Analysis status: Completed
- Number of tiles: 90
- Minimum value: 1
- Maximum value: 2
- Mean value: 1.1778
- Tile values: 74 tiles recorded 1; 16 tiles recorded 2

The returned UTC window covered 20:00–21:00.

**Finding:** The endpoint successfully processed the requested time range and returned tile-level results.

### 4.4 Persistence

The Persistence endpoint was tested using the same geographical area and time settings as the Exceedance test.

**Observed results:**
- HTTP response: 200 OK
- Analysis status: Completed
- Number of tiles: 90
- Minimum value: 1
- Maximum value: 2
- Mean value: 1.1778
- Tile values: 74 tiles recorded 1; 16 tiles recorded 2

The Persistence output was identical to the Exceedance output for this test.

**Finding:** The endpoint completed successfully. However, identical results from the two analytical functions do not establish that they behave identically. A longer test containing gaps between exceedance periods is needed to distinguish their behaviour reliably.

## 5. Dashboard Evaluation

The dashboard was examined for its visualization, environmental data, and monitoring capabilities.

### 5.1 Visualization

The following features were observed:

- Heatmap and polygon layers
- Opacity controls
- Celsius temperature display
- A 12-class legend
- Time simulation controls

The dashboard's demonstration statistics included:

| Metric | Value |
|---|---:|
| Maximum | 63.35°F |
| Minimum | 52.21°F |
| Range | 11.14°F |
| Mean | 57.76°F |
| Standard deviation | 1.45°F |

A Python-generated heatmap was also produced from the API evaluation data.

### 5.2 Environmental Data

The dashboard displayed several environmental measurements:

| Parameter | Observed value |
|---|---:|
| Humidity | 61.78% |
| Wet Bulb Globe | 18.93°F |
| Precipitation | 0 mm/hr |
| Air quality | N/A |
| Global Horizontal Irradiance (GHI) | 315.13 W/m² |
| Direct Normal Irradiance (DNI) | 724.41 W/m² |
| Diffuse Horizontal Irradiance (DHI) | 43.54 W/m² |

**Observations:**

- Humidity was flagged as high.
- Air quality was unavailable.
- Precipitation was displayed as zero, but it was unclear whether this represented a measured zero or missing data.
- The meaning and unit of the Wet Bulb Globe measurement require clarification.

### 5.3 Accuracy and Monitoring

The dashboard presented a proprietary seven-tier accuracy index, but no specific assigned accuracy score was identified during the evaluation.

Monitoring configuration was examined but not activated. Alert delivery and PDF reporting were therefore not verified.

## 6. Performance and Limitations

The following observations were recorded:

1. Some analytical requests, particularly Time of Measure, Exceedance, and Persistence, took more than five minutes to complete.
2. An initial single-hour Exceedance request returned HTTP 504 with an empty or non-JSON response. A subsequent range request completed successfully. The cause of the initial failure was not established.
3. Geographical coverage restrictions were observed.
4. Some environmental data fields lacked sufficient explanation.
5. Alert delivery and PDF export were not fully tested.
6. The identical Exceedance and Persistence outputs require further investigation using more varied time periods.

## 7. Recommendations

The following improvements are recommended:

1. **Improve API response handling:** Provide clearer error messages and more consistent responses when requests time out.
2. **Clarify geographical coverage:** Publish an accessible list or map of supported regions.
3. **Improve documentation:** Explain the meaning, units, and interpretation of environmental measurements.
4. **Validate analytical differences:** Test Persistence and Exceedance using longer periods with gaps in threshold exceedance.
5. **Improve performance:** Investigate long-running analytical requests and provide clearer progress information.
6. **Complete monitoring tests:** Verify alert delivery, report generation, and notification configuration.
7. **Improve data transparency:** Clearly distinguish between zero values and unavailable measurements.

## 8. Conclusion

The evaluation demonstrated that FortyGuard provides functional temperature-analysis endpoints and dashboard visualization capabilities.

All four analytical functions tested returned completed results in the successful test cases. The API also returned structured tile-level data that could be inspected and visualized using Python.

However, further testing is required to establish analytical accuracy, distinguish Persistence from Exceedance under more varied conditions, validate geographical coverage, and assess monitoring and reporting capabilities.

**Overall assessment:** The tested functionality is promising, but additional validation is required before making conclusions about the accuracy and reliability of the platform's temperature analytics.

## 9. Project Evidence

The accompanying GitHub repository contains the evaluation scripts and supporting outputs:

**Repository:** https://github.com/faith-amanze/fortyguard-product-evaluation

Key files include:

- `test_heatmap.py`
- `check_status.py`
- `inspect_exceedance.py`
- `inspect_persistence.py`
- `inspect_time_measure.py`
- `compare_time_results.py`
- `visualize_heatmap.py`
- JSON API result files
- `fortyguard_heatmap.png`

---

*This report documents observed product behaviour during the evaluation. It does not constitute independent scientific validation of temperature accuracy.*
