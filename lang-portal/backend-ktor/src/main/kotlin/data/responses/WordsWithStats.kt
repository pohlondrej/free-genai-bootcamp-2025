package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class WordWithStats(
    val japanese: String,
    val romaji: String,
    val english: String,
    val correctCount: Int,
    val wrongCount: Int
)