package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class WordDetails(
    val id: Int,
    val japanese: String,
    val romaji: String,
    val english: String,
    val stats: WordStats,
    val groups: List<GroupBasic>
)