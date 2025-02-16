package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class WordDetails(
    val id: Int,
    @SerialName("kanji") val japanese: String,
    val romaji: String,
    val english: String,
    @SerialName("correct_count") val correctCount: Int,
    @SerialName("wrong_count") val wrongCount: Int,
    val groups: List<GroupBasic>
)