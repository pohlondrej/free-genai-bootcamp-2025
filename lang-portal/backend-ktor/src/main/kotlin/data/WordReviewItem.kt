package com.pohlondrej.langportal.backend.data

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import java.time.LocalDateTime
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName

@Serializable
data class WordReviewItem(
    @SerialName("word_id") val wordId: Int,
    @SerialName("study_session_id") val studySessionId: Int,
    val correct: Boolean,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("created_at") val createdAt: LocalDateTime,
)