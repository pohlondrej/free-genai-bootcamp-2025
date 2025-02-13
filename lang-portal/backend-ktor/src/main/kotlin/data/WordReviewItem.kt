package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable
import kotlinx.datetime.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class WordReviewItem(
    @SerialName("word_id") val wordId: Int,
    @SerialName("study_session_id") val studySessionId: Int,
    val correct: Boolean,
    @SerialName("created_at") val createdAt: LocalDateTime,
)