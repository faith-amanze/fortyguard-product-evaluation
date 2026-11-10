# FortyGuard Product Evaluation Report

**Evaluator:** Faith Amanze  
**Products evaluated:** FortyGuard Temperature Dashboard, Temperature API, and Temperature MCP  
**Evaluation date:** November 2026  
**GitHub repository:** https://github.com/faith-amanze/fortyguard-product-evaluation

## 1. Executive Summary

I evaluated the FortyGuard Temperature Dashboard, Temperature API, and MCP integration to assess usability, functionality, documentation, reliability, and integration readiness.

The evaluation confirmed that the platform provides useful temperature analytics, including Temperature Condition Monitoring (TCM), Time of Measure, Exceedance, and Persistence. The API returned successful results for several Colorado-based tests and provided structured analytical outputs.

However, I identified areas that need improvement:

- The dashboard could communicate data provenance, accuracy, and environmental measurements more clearly.
- API requests may fail for locations outside supported coverage.
- One Exceedance request returned an HTTP 504 error.
- The MCP server exposed its tools and successfully executed the credit-balance operation, but its heatmap operation rejected three GeoJSON representations that its published schema says it supports.
- Further testing is required to establish MCP reliability, scalability, and AI-client compatibility.

Overall, FortyGuard has a useful technical foundation, but improvements to validation, documentation, and error handling would make the product more reliable and easier to integrate.

## 2. UX/UI

### Positive observations

- The dashboard presents temperature information through a map-based interface.
- Users can switch between heatmap and polygon layers.
- Temperature units can be changed to Celsius.
- The interface provides a 12-class legend.
- Opacity controls and time simulation help users explore the displayed data.
- Environmental information such as humidity, precipitation, and solar radiation is available.

### Areas for improvement

- Some data fields need clearer explanations and units.
- The dashboard should explain the source, timestamp, and provenance of displayed measurements.
- The proprietary seven-tier accuracy index should explain how scores are calculated and what each tier means.
- Missing environmental values should be distinguished from actual zero readings.
- The meaning of the Wet Bulb Globe measurement and its displayed unit should be clarified.

### Recommendation

Improve labels, tooltips, measurement definitions, and data-source information. Users should be able to understand what each measurement represents without consulting external documentation.

## 3. Navigation and Workflow

The dashboard provides access to map visualisation, analytics, and monitoring-related functions.

The main analytics tested were:

- Temperature Condition Monitoring (TCM)
- Time of Measure
- Exceedance
- Persistence

The Time of Measure, Exceedance, and Persistence operations took more than five minutes during testing, while Time Series and Distribution completed more quickly.

Some workflows, including monitor activation, alert delivery, PDF generation, and certain upload/download operations, were not fully verified.

### Recommendation

- Provide clearer progress indicators for long-running analytics.
- Show estimated processing time where possible.
- Make it easier to distinguish completed, pending, and failed operations.
- Provide clear confirmation when monitoring configurations and alerts are activated.

## 4. Dashboard Performance and Responsiveness

The dashboard successfully displayed temperature and environmental information for the tested area.

The demo heatmap displayed:

| Metric | Observed value |
|---|---:|
| Maximum temperature | 63.35°F |
| Minimum temperature | 52.21°F |
| Range | 11.14°F |
| Mean | 57.76°F |
| Standard deviation | 1.45 |

Time-consuming analytics were noticeably slower than the Time Series and Distribution operations.

A formal load test was not conducted, so these observations should not be interpreted as a complete assessment of system performance under heavy traffic.

### Recommendation

Improve feedback during long-running operations and conduct performance tests across different polygon sizes, date ranges, and concurrent requests.

## 5. API Structure and Design

The API provides access to temperature analytics through structured requests and responses.

The following operations were tested:

### Temperature Condition Monitoring (TCM)

A Colorado polygon request returned HTTP 200 and completed successfully.

Results:

- 90 tile features returned.
- Minimum temperature: 35.3936°C.
- Maximum temperature: 35.6786°C.
- Mean temperature: 35.5619°C.
- Standard deviation: 0.0441°C.

The histogram returned two temperature categories, with 82 and 8 observations respectively.

### Time of Measure

A request for July 15, 2024, at 14:00 Colorado local time returned a UTC window of 20:00.

A second request at 15:00 returned a UTC window of 21:00.

Both requests returned 90 cells, with the corresponding hour values represented consistently.

This was consistent with Colorado's UTC-6 offset in July.

### Exceedance

The test used:

- Threshold: 30°C.
- Direction: Above.
- Granularity: 100 metres.
- Date: July 15, 2024.
- Time range: 14:00–16:00 local time.

The request completed successfully and returned 90 tiles:

- 74 tiles recorded a value of 1.
- 16 tiles recorded a value of 2.
- Mean value: 1.1778.

The returned UTC window was 20:00–21:00.

An earlier single-hour Exceedance request returned HTTP 504 with an empty or non-JSON response. The cause could not be established.

### Persistence

The Persistence request used the same date, time range, threshold, direction, and granularity as the Exceedance test.

It completed successfully and returned:

- 90 tiles.
- 74 values of 1.
- 16 values of 2.
- Mean value of 1.1778.

The results matched the Exceedance test for this particular request. This does not establish that both analytics have identical behaviour; additional tests involving longer periods and gaps in threshold exceedance would be needed to distinguish their semantics.

### Geographic coverage

A New York polygon request returned HTTP 400 with the error `OUT_OF_COVERAGE`.

This indicates that API availability is geographically limited. The product should make supported coverage areas easy to identify before users submit requests.

### Recommendation

- Publish clear coverage information.
- Improve consistency in error responses.
- Provide examples for all analytics.
- Explain the difference between Exceedance and Persistence with practical examples.
- Include request limits and expected processing times in the documentation.

## 6. API Documentation

The API documentation provides an introduction to the available services and describes the request structure.

The documentation would benefit from:

- Complete request and response examples for each analytical operation.
- Clear explanations of required and optional parameters.
- More examples of valid GeoJSON Polygon, Feature, and FeatureCollection inputs.
- Clear descriptions of supported geographic coverage.
- Examples of common errors and how to resolve them.
- Information about processing time, rate limits, and credit consumption.
- More detailed explanations of returned statistical fields and units.

### Recommendation

Provide copy-and-run examples in Python, JavaScript, and PowerShell. Include valid GeoJSON examples and explain how to interpret the output.

## 7. Error Handling and Validation

The API returned a clear `OUT_OF_COVERAGE` response for the New York test.

However, the single-hour Exceedance request returned HTTP 504 without a useful structured explanation.

The MCP heatmap operation also revealed a reproducible input-validation issue.

### MCP heatmap validation test

The MCP tool list exposed a `heatmap` operation. Its published input schema described `polygon_aoi` as accepting a closed GeoJSON Polygon, Feature, or FeatureCollection.

I tested the same closed Colorado polygon using all three representations:

| Input representation | Result | Trace ID |
|---|---|---|
| GeoJSON Polygon | Rejected: `invalid_input` on `polygon_aoi` | `669750498e1f` |
| GeoJSON Feature | Rejected: `invalid_input` on `polygon_aoi` | `cb60295762bf` |
| GeoJSON FeatureCollection | Rejected: `invalid_input` on `polygon_aoi` | `87ad224ec880` |

All three attempts returned:

- Error category: `invalid_input`
- Error message: `The request input is invalid.`
- Field: `polygon_aoi`
- Processing latency: 0 ms
- Tool status: `error`

The requests were rejected before heatmap processing began. No successful heatmap activity was generated from these attempts.

The failures suggest a mismatch between the documented GeoJSON input contract and the server-side validation behaviour. The exact underlying cause could not be established from the available responses.

### Recommendation

- Verify that the MCP server accepts the GeoJSON formats stated in its schema.
- Return field-level validation details that explain what is wrong with the submitted polygon.
- Include valid sample payloads in the MCP documentation.
- Make API and MCP validation rules consistent.
- Return structured error details for timeouts and unsupported locations.

## 8. MCP Setup and Use with AI Tools

The FortyGuard MCP endpoint was configured and inspected using MCP Inspector.

**MCP endpoint:** `https://tos-mcp.app.fortyguard.com/mcp`

The server successfully exposed the following tools:

1. `credit_balance`
2. `env_params`
3. `heatmap`
4. `heatmap_read`
5. `monitoring`
6. `report`
7. `report_read`
8. `satellite`
9. `streetview`
10. `temperature_routing`
11. `temperature_routing_read`

### Successful test

The `credit_balance` tool executed successfully.

It returned:

- Available credits: 978,900.
- Status: `ok`.
- Cost: 0 credits.

This confirmed that the MCP endpoint was reachable, its tools could be discovered, and at least one tool could be invoked successfully.

### Failed test

The `heatmap` tool was tested using a Colorado polygon, TCM analytics, July 15, 2024, at 14:00 local time, and 100-metre granularity.

The tool rejected three GeoJSON representations with the same `invalid_input` error on `polygon_aoi`.

The repeated failure prevented successful end-to-end heatmap generation through MCP Inspector.

### AI-client compatibility limitation

Claude Code was installed and the FortyGuard MCP server was configured. However, interactive Claude Code use could not be completed because an authenticated Claude or Anthropic account was required.

MCP Inspector was therefore used to discover and invoke the server tools.

This means MCP protocol discovery and tool invocation were tested, but successful integration with an AI assistant such as Claude Code, Cursor, or Codex was not verified.

### Recommendation

- Resolve the heatmap input-validation issue.
- Provide a working end-to-end MCP example.
- Include setup instructions for Claude Code, Cursor, and other supported clients.
- Document which operations are free and which consume credits.
- Explain how users can retrieve results from asynchronous operations.

## 9. Scalability and Maintainability

The platform provides several analytical operations and a range of MCP tools, which suggests potential for integration into larger applications.

However, this evaluation did not include formal load testing, concurrency testing, or long-duration reliability testing.

The following areas should be considered:

- Consistent validation across API and MCP interfaces.
- Clear versioning and backward-compatibility policies.
- Predictable handling of long-running analytics.
- Documented geographic and request limits.
- Monitoring of failed requests and processing times.
- Clear separation between free and credit-consuming operations.

### Recommendation

Introduce automated integration tests for all MCP tools and API endpoints. Include valid and invalid GeoJSON test cases in the release pipeline.

## 10. Top Recommendations

1. **Fix MCP heatmap validation:** Ensure valid GeoJSON Polygon, Feature, and FeatureCollection inputs work as documented.
2. **Improve error handling:** Return actionable validation messages and consistent structured errors.
3. **Improve documentation:** Add complete examples, geographic coverage information, parameter explanations, and credit information.
4. **Improve dashboard clarity:** Explain measurement units, data provenance, accuracy scores, and missing values.
5. **Improve long-running workflows:** Provide better progress feedback and processing-time guidance.
6. **Expand automated testing:** Test different locations, polygon sizes, time ranges, and MCP tool operations.
7. **Verify AI-client integration:** Provide a working guide and test with supported AI clients.

## 11. Overall Conclusion

FortyGuard offers useful temperature analytics through its dashboard and API. The successful Colorado tests demonstrated that the API can return structured temperature measurements and analytical results.

The dashboard provides useful visualisation and environmental information, although some measurements and accuracy indicators need clearer explanations.

The MCP server was reachable, exposed 11 tools, and successfully executed the credit-balance operation. However, the heatmap operation repeatedly rejected all three documented GeoJSON input representations. This is an important integration issue because it prevented the main heatmap operation from completing through MCP.

My overall assessment is that FortyGuard has a promising technical foundation, but the product would benefit from stronger input validation, clearer documentation, improved error handling, and more complete integration testing.

## 12. Supporting Evidence

The evaluation scripts and API response files are available in the GitHub repository:

https://github.com/faith-amanze/fortyguard-product-evaluation

The repository contains Python scripts, JSON response samples, and a heatmap visualisation used during API evaluation.

MCP validation trace IDs:

- Polygon: `669750498e1f`
- Feature: `cb60295762bf`
- FeatureCollection: `87ad224ec880`

**Testing limitations:** This evaluation was not an independent scientific validation of temperature accuracy. Dashboard alert delivery, PDF generation, and formal scalability testing were not completed. MCP AI-client integration was not verified because interactive client authentication was unavailable.
