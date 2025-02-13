package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

@Serializable
data class Word(
    val id: Int,
    val japanese: String,
    val romaji: String,
    val english: String,
    val parts: JsonElement?,
)
