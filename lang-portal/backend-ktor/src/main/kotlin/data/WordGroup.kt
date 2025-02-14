package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class WordGroup(
    val id: Int,
    @SerialName("word_id") val wordId: Int,
    @SerialName("group_id") val groupId: Int,
)
