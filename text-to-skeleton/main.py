import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from spoken_to_signed.gloss_to_pose.lookup.fingerspelling_lookup import (
    FingerspellingPoseLookup,
)
from spoken_to_signed.gloss_to_pose.lookup.csv_lookup import CSVPoseLookup
from spoken_to_signed.gloss_to_pose import gloss_to_pose
from spoken_to_signed.bin import _pose_to_video
from utils import text_to_gloss__spacy_lemma

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Use absolute path for static files
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")
app.mount("/output", StaticFiles(directory=output_dir), name="output")


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
    lexicon_path = os.path.join(script_dir, "assets", "lexicon")
    output_path = os.path.join(script_dir, "output", "poses", "sample.pose")

    pose_lookup = CSVPoseLookup(
        lexicon_path,
        backup=fingerspelling_lookup,
    )
    print("glosses[0]", glosses[0])

    pose = gloss_to_pose(
        glosses[0],
        pose_lookup=pose_lookup,
        spoken_language="en",
        signed_language="ase",
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
        signed_language="ase",
        anonymize=False,
    )

    _pose_to_video(pose, output_path)

    return ""
