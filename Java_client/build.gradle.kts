plugins {
    java
}

group = "com.bimportal"
version = "1.0.0"

// Common configuration for all subprojects
subprojects {
    apply(plugin = "java")

    group = "com.bimportal"
    version = "1.0.0"

    java {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }

    repositories {
        mavenCentral()
    }

    // Common compiler options
    tasks.withType<JavaCompile> {
        options.encoding = "UTF-8"
        options.compilerArgs.addAll(listOf("-Xlint:unchecked", "-Xlint:deprecation"))
    }

    tasks.withType<Test> {
        useJUnitPlatform()
    }
}

// Root project configuration
repositories {
    mavenCentral()
}