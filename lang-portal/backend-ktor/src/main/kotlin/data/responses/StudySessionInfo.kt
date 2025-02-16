package com.pohlondrej.langportal.backend.data.responses

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import kotlinx.serialization.Serializable
import java.time.LocalDateTime

@Serializable
data class StudySessionInfo(
    val id: Int,
    val activityName: String,
    val groupName: String,
    @Serializable(with = LocalDateTimeSerializer::class)
    val startTime: LocalDateTime,
    @Serializable(with = LocalDateTimeSerializer::class)
    val endTime: LocalDateTime,
    val reviewItemsCount: Int
)

