# API contract

Send JSON to `https://api.argolink.io/v1/chat/completions` with `Authorization: Bearer $ARGOLINK_API_KEY`. The body must use `model: "glm-5.3"` and a non-empty `messages` array.

`reasoning_effort` accepts only `low`, `high`, or `max`; omit it for the documented default of `max`. Thinking cannot be disabled for this model.

A 4xx response means the request must be corrected. A 5xx or transport failure is an uncertain outcome; log the request ID and do not automatically submit a second paid request.
