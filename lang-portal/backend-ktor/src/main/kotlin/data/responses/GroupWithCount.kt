package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class GroupWithCount(
    val id: Int,
    val name: String,
    val wordCount: Int
)