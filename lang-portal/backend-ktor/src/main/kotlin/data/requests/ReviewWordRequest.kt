package com.pohlondrej.langportal.backend.data.requests

import kotlinx.serialization.Serializable

@Serializable
data class ReviewWordRequest(
    val correct: Boolean
)
