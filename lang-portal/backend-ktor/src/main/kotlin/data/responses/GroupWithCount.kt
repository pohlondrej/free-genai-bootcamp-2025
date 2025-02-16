package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class GroupWithCount(
    val id: Int,
    @SerialName("group_name") val name: String,
    @SerialName("word_count") val wordCount: Int
)