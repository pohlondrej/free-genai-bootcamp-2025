package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class SuccessResponse(
    val success: Boolean,
    val message: String
)

