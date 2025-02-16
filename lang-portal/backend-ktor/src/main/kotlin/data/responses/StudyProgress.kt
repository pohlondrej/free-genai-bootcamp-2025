package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class StudyProgress(
    @SerialName("total_words_studied") val totalWordsStudied: Int,
    @SerialName("total_available_words") val totalAvailableWords: Int
)