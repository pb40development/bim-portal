plugins {
    java
    application
    id("org.springframework.boot") version "3.4.0"
    id("io.spring.dependency-management") version "1.1.6"
}

group = "com.bimportal.hackathon"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    // Dependency on the BIM Portal enhanced client
    implementation(project(":bim-portal-enhanced"))

    // Spring Boot starters for web applications (optional for hackathon)
    implementation("org.springframework.boot:spring-boot-starter")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-json")

    // Additional utilities for hackathon development
    implementation("org.apache.commons:commons-lang3:3.12.0")
    implementation("org.apache.commons:commons-csv:1.10.0")
    implementation("com.google.guava:guava:32.1.2-jre")

    // JSON processing
    implementation("com.fasterxml.jackson.core:jackson-databind:2.15.2")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.2")

    // Logging
    implementation("org.slf4j:slf4j-api:2.0.9")
    implementation("ch.qos.logback:logback-classic:1.4.11")

    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("org.mockito:mockito-core:5.5.0")
    testImplementation("org.assertj:assertj-core:3.24.2")
}

application {
    mainClass.set("com.bimportal.hackathon.HackathonApplication")
}

// Custom tasks for different hackathon scenarios
tasks.register<JavaExec>("runBasicExample") {
    group = "hackathon"
    description = "Run basic BIM Portal API example"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.bimportal.hackathon.examples.BasicExample")
}


// Resource processing
tasks.processResources {
    filesMatching("application.properties") {
        expand(project.properties)
    }
}

tasks.test {
    useJUnitPlatform()
}

// Custom fat JAR task for easy deployment
tasks.register<Jar>("hackathonJar") {
    group = "hackathon"
    description = "Create a fat JAR for hackathon deployment"
    archiveClassifier.set("hackathon")
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE

    manifest {
        attributes["Main-Class"] = "com.bimportal.hackathon.HackathonApplication"
    }

    from(configurations.runtimeClasspath.get().map {
        if (it.isDirectory) it else zipTree(it)
    })

    with(tasks.jar.get() as CopySpec)
}