package com.pohlondrej.langportal.backend.data.responses

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import kotlinx.serialization.Serializable
import java.time.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class StudySessionInfo(
    val id: Int,
    @SerialName("activity_name") val activityName: String,
    @SerialName("group_name") val groupName: String,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("start_time") val startTime: LocalDateTime,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("end_time") val endTime: LocalDateTime,
    @SerialName("review_items_count") val reviewItemsCount: Int
)

