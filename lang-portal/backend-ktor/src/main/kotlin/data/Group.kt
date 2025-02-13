package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable

@Serializable
data class Group(
    val id: Int,
    val name: String,
)
