# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.videointelligence.v1p2beta1",
    manifest={
        "Feature",
        "LabelDetectionMode",
        "Likelihood",
        "AnnotateVideoRequest",
        "VideoContext",
        "LabelDetectionConfig",
        "ShotChangeDetectionConfig",
        "ExplicitContentDetectionConfig",
        "TextDetectionConfig",
        "VideoSegment",
        "LabelSegment",
        "LabelFrame",
        "Entity",
        "LabelAnnotation",
        "ExplicitContentFrame",
        "ExplicitContentAnnotation",
        "NormalizedBoundingBox",
        "VideoAnnotationResults",
        "AnnotateVideoResponse",
        "VideoAnnotationProgress",
        "AnnotateVideoProgress",
        "NormalizedVertex",
        "NormalizedBoundingPoly",
        "TextSegment",
        "TextFrame",
        "TextAnnotation",
        "ObjectTrackingFrame",
        "ObjectTrackingAnnotation",
    },
)


class Feature(proto.Enum):
    r"""Video annotation feature."""
    FEATURE_UNSPECIFIED = 0
    LABEL_DETECTION = 1
    SHOT_CHANGE_DETECTION = 2
    EXPLICIT_CONTENT_DETECTION = 3
    TEXT_DETECTION = 7
    OBJECT_TRACKING = 9


class LabelDetectionMode(proto.Enum):
    r"""Label detection mode."""
    LABEL_DETECTION_MODE_UNSPECIFIED = 0
    SHOT_MODE = 1
    FRAME_MODE = 2
    SHOT_AND_FRAME_MODE = 3


class Likelihood(proto.Enum):
    r"""Bucketized representation of likelihood."""
    LIKELIHOOD_UNSPECIFIED = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5


class AnnotateVideoRequest(proto.Message):
    r"""Video annotation request.
    Attributes:
        input_uri (str):
            Input video location. Currently, only `Google Cloud
            Storage <https://cloud.google.com/storage/>`__ URIs are
            supported, which must be specified in the following format:
            ``gs://bucket-id/object-id`` (other URI formats return
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]).
            For more information, see `Request
            URIs <https://cloud.google.com/storage/docs/request-endpoints>`__.
            A video URI may include wildcards in ``object-id``, and thus
            identify multiple videos. Supported wildcards: '*' to match
            0 or more characters; '?' to match 1 character. If unset,
            the input video should be embedded in the request as
            ``input_content``. If set, ``input_content`` should be
            unset.
        input_content (bytes):
            The video data bytes. If unset, the input video(s) should be
            specified via ``input_uri``. If set, ``input_uri`` should be
            unset.
        features (Sequence[google.cloud.videointelligence_v1p2beta1.types.Feature]):
            Required. Requested video annotation
            features.
        video_context (google.cloud.videointelligence_v1p2beta1.types.VideoContext):
            Additional video context and/or feature-
            pecific parameters.
        output_uri (str):
            Optional. Location where the output (in JSON format) should
            be stored. Currently, only `Google Cloud
            Storage <https://cloud.google.com/storage/>`__ URIs are
            supported, which must be specified in the following format:
            ``gs://bucket-id/object-id`` (other URI formats return
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]).
            For more information, see `Request
            URIs <https://cloud.google.com/storage/docs/request-endpoints>`__.
        location_id (str):
            Optional. Cloud region where annotation should take place.
            Supported cloud regions: ``us-east1``, ``us-west1``,
            ``europe-west1``, ``asia-east1``. If no region is specified,
            a region will be determined based on video file location.
    """

    input_uri = proto.Field(proto.STRING, number=1,)
    input_content = proto.Field(proto.BYTES, number=6,)
    features = proto.RepeatedField(proto.ENUM, number=2, enum="Feature",)
    video_context = proto.Field(proto.MESSAGE, number=3, message="VideoContext",)
    output_uri = proto.Field(proto.STRING, number=4,)
    location_id = proto.Field(proto.STRING, number=5,)


class VideoContext(proto.Message):
    r"""Video context and/or feature-specific parameters.
    Attributes:
        segments (Sequence[google.cloud.videointelligence_v1p2beta1.types.VideoSegment]):
            Video segments to annotate. The segments may
            overlap and are not required to be contiguous or
            span the whole video. If unspecified, each video
            is treated as a single segment.
        label_detection_config (google.cloud.videointelligence_v1p2beta1.types.LabelDetectionConfig):
            Config for LABEL_DETECTION.
        shot_change_detection_config (google.cloud.videointelligence_v1p2beta1.types.ShotChangeDetectionConfig):
            Config for SHOT_CHANGE_DETECTION.
        explicit_content_detection_config (google.cloud.videointelligence_v1p2beta1.types.ExplicitContentDetectionConfig):
            Config for EXPLICIT_CONTENT_DETECTION.
        text_detection_config (google.cloud.videointelligence_v1p2beta1.types.TextDetectionConfig):
            Config for TEXT_DETECTION.
    """

    segments = proto.RepeatedField(proto.MESSAGE, number=1, message="VideoSegment",)
    label_detection_config = proto.Field(
        proto.MESSAGE, number=2, message="LabelDetectionConfig",
    )
    shot_change_detection_config = proto.Field(
        proto.MESSAGE, number=3, message="ShotChangeDetectionConfig",
    )
    explicit_content_detection_config = proto.Field(
        proto.MESSAGE, number=4, message="ExplicitContentDetectionConfig",
    )
    text_detection_config = proto.Field(
        proto.MESSAGE, number=8, message="TextDetectionConfig",
    )


class LabelDetectionConfig(proto.Message):
    r"""Config for LABEL_DETECTION.
    Attributes:
        label_detection_mode (google.cloud.videointelligence_v1p2beta1.types.LabelDetectionMode):
            What labels should be detected with LABEL_DETECTION, in
            addition to video-level labels or segment-level labels. If
            unspecified, defaults to ``SHOT_MODE``.
        stationary_camera (bool):
            Whether the video has been shot from a stationary (i.e.
            non-moving) camera. When set to true, might improve
            detection accuracy for moving objects. Should be used with
            ``SHOT_AND_FRAME_MODE`` enabled.
        model (str):
            Model to use for label detection.
            Supported values: "builtin/stable" (the default
            if unset) and "builtin/latest".
    """

    label_detection_mode = proto.Field(proto.ENUM, number=1, enum="LabelDetectionMode",)
    stationary_camera = proto.Field(proto.BOOL, number=2,)
    model = proto.Field(proto.STRING, number=3,)


class ShotChangeDetectionConfig(proto.Message):
    r"""Config for SHOT_CHANGE_DETECTION.
    Attributes:
        model (str):
            Model to use for shot change detection.
            Supported values: "builtin/stable" (the default
            if unset) and "builtin/latest".
    """

    model = proto.Field(proto.STRING, number=1,)


class ExplicitContentDetectionConfig(proto.Message):
    r"""Config for EXPLICIT_CONTENT_DETECTION.
    Attributes:
        model (str):
            Model to use for explicit content detection.
            Supported values: "builtin/stable" (the default
            if unset) and "builtin/latest".
    """

    model = proto.Field(proto.STRING, number=1,)


class TextDetectionConfig(proto.Message):
    r"""Config for TEXT_DETECTION.
    Attributes:
        language_hints (Sequence[str]):
            Language hint can be specified if the
            language to be detected is known a priori. It
            can increase the accuracy of the detection.
            Language hint must be language code in BCP-47
            format.

            Automatic language detection is performed if no
            hint is provided.
    """

    language_hints = proto.RepeatedField(proto.STRING, number=1,)


class VideoSegment(proto.Message):
    r"""Video segment.
    Attributes:
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Time-offset, relative to the beginning of the
            video, corresponding to the start of the segment
            (inclusive).
        end_time_offset (google.protobuf.duration_pb2.Duration):
            Time-offset, relative to the beginning of the
            video, corresponding to the end of the segment
            (inclusive).
    """

    start_time_offset = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    end_time_offset = proto.Field(
        proto.MESSAGE, number=2, message=duration_pb2.Duration,
    )


class LabelSegment(proto.Message):
    r"""Video segment level annotation results for label detection.
    Attributes:
        segment (google.cloud.videointelligence_v1p2beta1.types.VideoSegment):
            Video segment where a label was detected.
        confidence (float):
            Confidence that the label is accurate. Range: [0, 1].
    """

    segment = proto.Field(proto.MESSAGE, number=1, message="VideoSegment",)
    confidence = proto.Field(proto.FLOAT, number=2,)


class LabelFrame(proto.Message):
    r"""Video frame level annotation results for label detection.
    Attributes:
        time_offset (google.protobuf.duration_pb2.Duration):
            Time-offset, relative to the beginning of the
            video, corresponding to the video frame for this
            location.
        confidence (float):
            Confidence that the label is accurate. Range: [0, 1].
    """

    time_offset = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    confidence = proto.Field(proto.FLOAT, number=2,)


class Entity(proto.Message):
    r"""Detected entity from video analysis.
    Attributes:
        entity_id (str):
            Opaque entity ID. Some IDs may be available in `Google
            Knowledge Graph Search
            API <https://developers.google.com/knowledge-graph/>`__.
        description (str):
            Textual description, e.g. ``Fixed-gear bicycle``.
        language_code (str):
            Language code for ``description`` in BCP-47 format.
    """

    entity_id = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    language_code = proto.Field(proto.STRING, number=3,)


class LabelAnnotation(proto.Message):
    r"""Label annotation.
    Attributes:
        entity (google.cloud.videointelligence_v1p2beta1.types.Entity):
            Detected entity.
        category_entities (Sequence[google.cloud.videointelligence_v1p2beta1.types.Entity]):
            Common categories for the detected entity. E.g. when the
            label is ``Terrier`` the category is likely ``dog``. And in
            some cases there might be more than one categories e.g.
            ``Terrier`` could also be a ``pet``.
        segments (Sequence[google.cloud.videointelligence_v1p2beta1.types.LabelSegment]):
            All video segments where a label was
            detected.
        frames (Sequence[google.cloud.videointelligence_v1p2beta1.types.LabelFrame]):
            All video frames where a label was detected.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message="Entity",)
    category_entities = proto.RepeatedField(proto.MESSAGE, number=2, message="Entity",)
    segments = proto.RepeatedField(proto.MESSAGE, number=3, message="LabelSegment",)
    frames = proto.RepeatedField(proto.MESSAGE, number=4, message="LabelFrame",)


class ExplicitContentFrame(proto.Message):
    r"""Video frame level annotation results for explicit content.
    Attributes:
        time_offset (google.protobuf.duration_pb2.Duration):
            Time-offset, relative to the beginning of the
            video, corresponding to the video frame for this
            location.
        pornography_likelihood (google.cloud.videointelligence_v1p2beta1.types.Likelihood):
            Likelihood of the pornography content..
    """

    time_offset = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    pornography_likelihood = proto.Field(proto.ENUM, number=2, enum="Likelihood",)


class ExplicitContentAnnotation(proto.Message):
    r"""Explicit content annotation (based on per-frame visual
    signals only). If no explicit content has been detected in a
    frame, no annotations are present for that frame.

    Attributes:
        frames (Sequence[google.cloud.videointelligence_v1p2beta1.types.ExplicitContentFrame]):
            All video frames where explicit content was
            detected.
    """

    frames = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ExplicitContentFrame",
    )


class NormalizedBoundingBox(proto.Message):
    r"""Normalized bounding box. The normalized vertex coordinates are
    relative to the original image. Range: [0, 1].

    Attributes:
        left (float):
            Left X coordinate.
        top (float):
            Top Y coordinate.
        right (float):
            Right X coordinate.
        bottom (float):
            Bottom Y coordinate.
    """

    left = proto.Field(proto.FLOAT, number=1,)
    top = proto.Field(proto.FLOAT, number=2,)
    right = proto.Field(proto.FLOAT, number=3,)
    bottom = proto.Field(proto.FLOAT, number=4,)


class VideoAnnotationResults(proto.Message):
    r"""Annotation results for a single video.
    Attributes:
        input_uri (str):
            Video file location in `Google Cloud
            Storage <https://cloud.google.com/storage/>`__.
        segment_label_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.LabelAnnotation]):
            Label annotations on video level or user
            specified segment level. There is exactly one
            element for each unique label.
        shot_label_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.LabelAnnotation]):
            Label annotations on shot level.
            There is exactly one element for each unique
            label.
        frame_label_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.LabelAnnotation]):
            Label annotations on frame level.
            There is exactly one element for each unique
            label.
        shot_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.VideoSegment]):
            Shot annotations. Each shot is represented as
            a video segment.
        explicit_annotation (google.cloud.videointelligence_v1p2beta1.types.ExplicitContentAnnotation):
            Explicit content annotation.
        text_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.TextAnnotation]):
            OCR text detection and tracking.
            Annotations for list of detected text snippets.
            Each will have list of frame information
            associated with it.
        object_annotations (Sequence[google.cloud.videointelligence_v1p2beta1.types.ObjectTrackingAnnotation]):
            Annotations for list of objects detected and
            tracked in video.
        error (google.rpc.status_pb2.Status):
            If set, indicates an error. Note that for a single
            ``AnnotateVideoRequest`` some videos may succeed and some
            may fail.
    """

    input_uri = proto.Field(proto.STRING, number=1,)
    segment_label_annotations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="LabelAnnotation",
    )
    shot_label_annotations = proto.RepeatedField(
        proto.MESSAGE, number=3, message="LabelAnnotation",
    )
    frame_label_annotations = proto.RepeatedField(
        proto.MESSAGE, number=4, message="LabelAnnotation",
    )
    shot_annotations = proto.RepeatedField(
        proto.MESSAGE, number=6, message="VideoSegment",
    )
    explicit_annotation = proto.Field(
        proto.MESSAGE, number=7, message="ExplicitContentAnnotation",
    )
    text_annotations = proto.RepeatedField(
        proto.MESSAGE, number=12, message="TextAnnotation",
    )
    object_annotations = proto.RepeatedField(
        proto.MESSAGE, number=14, message="ObjectTrackingAnnotation",
    )
    error = proto.Field(proto.MESSAGE, number=9, message=status_pb2.Status,)


class AnnotateVideoResponse(proto.Message):
    r"""Video annotation response. Included in the ``response`` field of the
    ``Operation`` returned by the ``GetOperation`` call of the
    ``google::longrunning::Operations`` service.

    Attributes:
        annotation_results (Sequence[google.cloud.videointelligence_v1p2beta1.types.VideoAnnotationResults]):
            Annotation results for all videos specified in
            ``AnnotateVideoRequest``.
    """

    annotation_results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="VideoAnnotationResults",
    )


class VideoAnnotationProgress(proto.Message):
    r"""Annotation progress for a single video.
    Attributes:
        input_uri (str):
            Video file location in `Google Cloud
            Storage <https://cloud.google.com/storage/>`__.
        progress_percent (int):
            Approximate percentage processed thus far.
            Guaranteed to be 100 when fully processed.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when the request was received.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Time of the most recent update.
    """

    input_uri = proto.Field(proto.STRING, number=1,)
    progress_percent = proto.Field(proto.INT32, number=2,)
    start_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class AnnotateVideoProgress(proto.Message):
    r"""Video annotation progress. Included in the ``metadata`` field of the
    ``Operation`` returned by the ``GetOperation`` call of the
    ``google::longrunning::Operations`` service.

    Attributes:
        annotation_progress (Sequence[google.cloud.videointelligence_v1p2beta1.types.VideoAnnotationProgress]):
            Progress metadata for all videos specified in
            ``AnnotateVideoRequest``.
    """

    annotation_progress = proto.RepeatedField(
        proto.MESSAGE, number=1, message="VideoAnnotationProgress",
    )


class NormalizedVertex(proto.Message):
    r"""A vertex represents a 2D point in the image.
    NOTE: the normalized vertex coordinates are relative to the
    original image and range from 0 to 1.

    Attributes:
        x (float):
            X coordinate.
        y (float):
            Y coordinate.
    """

    x = proto.Field(proto.FLOAT, number=1,)
    y = proto.Field(proto.FLOAT, number=2,)


class NormalizedBoundingPoly(proto.Message):
    r"""Normalized bounding polygon for text (that might not be aligned with
    axis). Contains list of the corner points in clockwise order
    starting from top-left corner. For example, for a rectangular
    bounding box: When the text is horizontal it might look like: 0----1
    \| \| 3----2

    When it's clockwise rotated 180 degrees around the top-left corner
    it becomes: 2----3 \| \| 1----0

    and the vertex order will still be (0, 1, 2, 3). Note that values
    can be less than 0, or greater than 1 due to trignometric
    calculations for location of the box.

    Attributes:
        vertices (Sequence[google.cloud.videointelligence_v1p2beta1.types.NormalizedVertex]):
            Normalized vertices of the bounding polygon.
    """

    vertices = proto.RepeatedField(proto.MESSAGE, number=1, message="NormalizedVertex",)


class TextSegment(proto.Message):
    r"""Video segment level annotation results for text detection.
    Attributes:
        segment (google.cloud.videointelligence_v1p2beta1.types.VideoSegment):
            Video segment where a text snippet was
            detected.
        confidence (float):
            Confidence for the track of detected text. It
            is calculated as the highest over all frames
            where OCR detected text appears.
        frames (Sequence[google.cloud.videointelligence_v1p2beta1.types.TextFrame]):
            Information related to the frames where OCR
            detected text appears.
    """

    segment = proto.Field(proto.MESSAGE, number=1, message="VideoSegment",)
    confidence = proto.Field(proto.FLOAT, number=2,)
    frames = proto.RepeatedField(proto.MESSAGE, number=3, message="TextFrame",)


class TextFrame(proto.Message):
    r"""Video frame level annotation results for text annotation
    (OCR). Contains information regarding timestamp and bounding box
    locations for the frames containing detected OCR text snippets.

    Attributes:
        rotated_bounding_box (google.cloud.videointelligence_v1p2beta1.types.NormalizedBoundingPoly):
            Bounding polygon of the detected text for
            this frame.
        time_offset (google.protobuf.duration_pb2.Duration):
            Timestamp of this frame.
    """

    rotated_bounding_box = proto.Field(
        proto.MESSAGE, number=1, message="NormalizedBoundingPoly",
    )
    time_offset = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)


class TextAnnotation(proto.Message):
    r"""Annotations related to one detected OCR text snippet. This
    will contain the corresponding text, confidence value, and frame
    level information for each detection.

    Attributes:
        text (str):
            The detected text.
        segments (Sequence[google.cloud.videointelligence_v1p2beta1.types.TextSegment]):
            All video segments where OCR detected text
            appears.
    """

    text = proto.Field(proto.STRING, number=1,)
    segments = proto.RepeatedField(proto.MESSAGE, number=2, message="TextSegment",)


class ObjectTrackingFrame(proto.Message):
    r"""Video frame level annotations for object detection and
    tracking. This field stores per frame location, time offset, and
    confidence.

    Attributes:
        normalized_bounding_box (google.cloud.videointelligence_v1p2beta1.types.NormalizedBoundingBox):
            The normalized bounding box location of this
            object track for the frame.
        time_offset (google.protobuf.duration_pb2.Duration):
            The timestamp of the frame in microseconds.
    """

    normalized_bounding_box = proto.Field(
        proto.MESSAGE, number=1, message="NormalizedBoundingBox",
    )
    time_offset = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)


class ObjectTrackingAnnotation(proto.Message):
    r"""Annotations corresponding to one tracked object.
    Attributes:
        entity (google.cloud.videointelligence_v1p2beta1.types.Entity):
            Entity to specify the object category that
            this track is labeled as.
        confidence (float):
            Object category's labeling confidence of this
            track.
        frames (Sequence[google.cloud.videointelligence_v1p2beta1.types.ObjectTrackingFrame]):
            Information corresponding to all frames where
            this object track appears.
        segment (google.cloud.videointelligence_v1p2beta1.types.VideoSegment):
            Each object track corresponds to one video
            segment where it appears.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message="Entity",)
    confidence = proto.Field(proto.FLOAT, number=4,)
    frames = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ObjectTrackingFrame",
    )
    segment = proto.Field(proto.MESSAGE, number=3, message="VideoSegment",)


__all__ = tuple(sorted(__protobuf__.manifest))
