# delernen release (R8) 规则
# 说明：App 用 org.json 手动解析 assets JSON，没有反射式序列化；
# Room / Compose / Navigation / Lifecycle 都自带 consumer rules，这里只做兜底。

# ---- Room ----
-keep class * extends androidx.room.RoomDatabase { <init>(); }
-keep @androidx.room.Entity class * { *; }
-keep @androidx.room.Dao interface * { *; }
-dontwarn androidx.room.paging.**

# 实体/模型保留字段名（Room 生成代码按名访问；数据模型调试时可读）
-keep class com.astemo.delernen.data.db.** { *; }

# ---- kotlinx.serialization（当前未使用；以后引入时这些规则即生效，无副作用）----
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt
-keepclassmembers class kotlinx.serialization.json.** { *** Companion; }
-keepclasseswithmembers class kotlinx.serialization.json.** { kotlinx.serialization.KSerializer serializer(...); }
-keep,includedescriptorclasses class com.astemo.delernen.**$$serializer { *; }
-keepclassmembers class com.astemo.delernen.** { *** Companion; }
-keepclasseswithmembers class com.astemo.delernen.** { kotlinx.serialization.KSerializer serializer(...); }
-dontwarn kotlinx.serialization.**

# 崩溃栈可读：保留行号，源文件名改写
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
