package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class GroupDetails(
    val id: Int,
    @SerialName("group_name") val name: String,
    val stats: GroupStats
)