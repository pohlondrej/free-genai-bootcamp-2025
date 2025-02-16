package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class StudyActivityCreated(
    val id: Int,
    @SerialName("group_id") val groupId: Int
)

