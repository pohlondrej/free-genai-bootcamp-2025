package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class GroupStats(
    @SerialName("word_count") val totalWordCount: Int
)