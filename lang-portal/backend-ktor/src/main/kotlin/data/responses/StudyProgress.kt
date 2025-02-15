package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class StudyProgress(
    val totalWordsStudied: Int,
    val totalAvailableWords: Int
)