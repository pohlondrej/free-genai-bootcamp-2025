package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class WordStats(
    val correctCount: Int,
    val wrongCount: Int
)
