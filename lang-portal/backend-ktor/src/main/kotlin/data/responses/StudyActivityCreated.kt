package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class StudyActivityCreated(
    val id: Int,
    val groupId: Int
)

