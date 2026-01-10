import os
from fastapi import FastAPI, Response
from spoken_to_signed.gloss_to_pose.lookup.fingerspelling_lookup import (
    FingerspellingPoseLookup,
)
from spoken_to_signed.gloss_to_pose.lookup.csv_lookup import CSVPoseLookup
from spoken_to_signed.gloss_to_pose import gloss_to_pose
from spoken_to_signed.bin import _pose_to_video
from utils import text_to_gloss__spacy_lemma

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


@app.get("/text-to-gloss")
async def text_to_gloss(text: str):
    glosses = text_to_gloss__spacy_lemma(text, language="en", ignore_punctuation=True)

    return glosses


@app.get("/text-to-pose")
async def text_to_pose(text: str):
    glosses = text_to_gloss__spacy_lemma(text, language="en", ignore_punctuation=True)
    fingerspelling_lookup = FingerspellingPoseLookup()

    # Use absolute path based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lexicon_path = os.path.join(script_dir, "assets", "dummy_lexicon")
    output_path = os.path.join(script_dir, "output", "poses", "sample.pose")

    pose_lookup = CSVPoseLookup(
        lexicon_path,
        backup=fingerspelling_lookup,
    )

    pose = gloss_to_pose(
        glosses[0],
        pose_lookup=pose_lookup,
        spoken_language="en",
        signed_language="asl",
        anonymize=False,
    )

    with open(output_path, "wb") as f:
        pose.write(f)

    return Response()


@app.get("/text-to-video")
async def text_to_video(text: str):
    glosses = text_to_gloss__spacy_lemma(text, language="en", ignore_punctuation=True)
    fingerspelling_lookup = FingerspellingPoseLookup()

    # Use absolute path based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lexicon_path = os.path.join(script_dir, "assets", "lexicon")
    output_path = os.path.join(script_dir, "output", "videos", "sample.mp4")

    pose_lookup = CSVPoseLookup(
        lexicon_path,
        backup=fingerspelling_lookup,
    )

    pose = gloss_to_pose(
        glosses[0],
        pose_lookup=pose_lookup,
        spoken_language="en",
        signed_language="asl",
        anonymize=False,
    )

    _pose_to_video(pose, output_path)

    return ''
