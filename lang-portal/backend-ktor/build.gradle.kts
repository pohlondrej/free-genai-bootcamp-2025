
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.ktor)
    alias(libs.plugins.kotlin.plugin.serialization)
}

group = "com.pohlondrej.langportal.backend"
version = "0.0.1"

application {
    mainClass.set("io.ktor.server.netty.EngineMain")

    val isDevelopment: Boolean = project.ext.has("development")
    applicationDefaultJvmArgs = listOf("-Dio.ktor.development=$isDevelopment")
}

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(23)
}

dependencies {
    implementation(libs.ktor.server.core)
    implementation(libs.ktor.server.swagger)
    implementation(libs.ktor.server.cors)
    implementation(libs.ktor.server.content.negotiation)
    implementation(libs.ktor.serialization.gson)
    implementation(libs.ktor.serialization.kotlinx.json)
    implementation(libs.koin.ktor)
    implementation(libs.koin.logger.slf4j)
    implementation(libs.ktor.server.netty)
    implementation(libs.logback.classic)
    implementation(libs.ktor.server.config.yaml)
    implementation(libs.kotlinx.datetime)
    implementation(libs.exposed.core)
    implementation(libs.exposed.dao)
    implementation(libs.exposed.jdbc)
    implementation(libs.exposed.java.time)
    implementation(libs.sqlite.jdbc)
    testImplementation(libs.ktor.server.test.host)
    testImplementation(libs.kotlin.test.junit)
}

fun runDbQuery(dbFile: File, queryFile: File) {
    val process = ProcessBuilder("sqlite3", dbFile.absolutePath)
        .redirectInput(queryFile)
        .redirectOutput(ProcessBuilder.Redirect.INHERIT)
        .redirectError(ProcessBuilder.Redirect.INHERIT)
        .start()

    process.waitFor()

    if (process.exitValue() == 0) {
        println("Database query ${queryFile.absolutePath} succeeded!")
    } else {
        println("Database initialization failed. Check error output.")
    }
}

tasks.register("initializeDb") {
    dependsOn("build")
    doLast {
        val dbFile = file("words.db")
        val initSqlFile = file("migrations/0001_init.sql")
        val dbTestEntries = file("migrations/0002_seed_data.sql")

        if (dbFile.exists()) {
            dbFile.delete()
        }

        runDbQuery(dbFile, initSqlFile)
        runDbQuery(dbFile, dbTestEntries)
    }
}

tasks.named<JavaExec>("run") {
    dependsOn("build")
    dependsOn("initializeDb")
    jvmArgs = listOf("-Dio.ktor.development=true")
}
