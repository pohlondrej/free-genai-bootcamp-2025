package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class GroupDetails(
    val id: Int,
    val name: String,
    val stats: GroupStats
)