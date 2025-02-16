package com.pohlondrej.langportal.backend.data

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import kotlinx.serialization.Serializable
import java.time.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class StudySession(
    val id: Int,
    @SerialName("group_id") val groupId: Int,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("created_at") val createdAt: LocalDateTime,
    @SerialName("study_activity_id") val studyActivityId: Int,
)
