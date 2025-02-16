package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class GroupBasic(
    val id: Int,
    val name: String
)