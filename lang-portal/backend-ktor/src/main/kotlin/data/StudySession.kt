package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable
import kotlinx.datetime.Instant
import kotlinx.serialization.SerialName

@Serializable
data class StudySession(
    val id: Int,
    @SerialName("group_id") val groupId: Int,
    @SerialName("created_at") val createdAt: Instant,
    @SerialName("study_activity_id") val studyActivityId: Int,
)
