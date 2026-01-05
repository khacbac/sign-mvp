#!/usr/bin/env python3
"""
WLASL Integration Demo

Demonstrates the WLASL video integration for sign language translation.
"""

from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def demo_wlasl_integration():
    """Demonstrate the WLASL integration"""

    print("🎬 WLASL Human Video Integration Demo")
    print("=" * 50)

    # Test 1: Gloss Mapper
    print("\n1. Testing Gloss Mapper...")
    from avatar_engines.human_video.gloss_mapper import get_gloss_mapper

    mapper = get_gloss_mapper()
    print(f"   ✓ Loaded {len(mapper.get_gloss_vocabulary())} glosses from WLASL")

    # Test specific glosses
    test_glosses = ["BOOK", "DRINK", "LOVE", "WATER", "COMPUTER"]
    for gloss in test_glosses:
        if mapper.gloss_exists(gloss):
            best_video = mapper.get_best_video(gloss)
            video_count = mapper.get_video_count(gloss)
            print(f"   ✓ '{gloss}': {video_count} videos available")
            print(f"     Best source: {best_video['source']}")
            print(f"     URL: {best_video['url'][:60]}...")
        else:
            print(f"   ✗ '{gloss}': Not found in dataset")

    # Test 2: Video Loader
    print(f"\n2. Testing Video Loader...")
    from avatar_engines.human_video.video_loader import create_video_loader
    from avatar_engines.human_video.config import VIDEO_CACHE_DIR

    loader = create_video_loader()
    print(f"   ✓ Cache directory: {VIDEO_CACHE_DIR}")
    print(f"   ✓ Cache exists: {VIDEO_CACHE_DIR.exists()}")

    cache_info = loader.get_cache_info()
    print(f"   ✓ Current cache size: {cache_info['total_size_gb']:.2f} GB")
    print(f"   ✓ Cached videos: {cache_info['video_count']}")

    # Test 3: Video Download (optional - requires internet)
    print(f"\n3. Testing Video Download...")
    test_gloss = "HELLO"
    best_video = mapper.get_best_video(test_gloss)

    if best_video:
        video_id = best_video['video_id']
        video_url = best_video['url']

        print(f"   Attempting to download '{test_gloss}' (video_id: {video_id})")
        print(f"   URL: {video_url}")

        try:
            video_path = loader.download_video(video_url, video_id)
            if video_path and video_path.exists():
                print(f"   ✓ Successfully downloaded to: {video_path}")
                print(f"   ✓ File size: {video_path.stat().st_size / 1024:.0f} KB")
            else:
                print(f"   ✗ Download failed (video may not be available)")
        except Exception as e:
            print(f"   ✗ Download error: {e}")

    # Test 4: Missing Gloss
    print(f"\n4. Testing Missing Gloss Handling...")
    missing_gloss = "COMPUTING"
    if not mapper.gloss_exists(missing_gloss):
        similar = mapper.find_similar_glosses(missing_gloss)
        print(f"   ✓ '{missing_gloss}' not found")
        print(f"   ✓ Similar glosses: {similar[:5]}")

    # Test 5: Full Pipeline Example
    print(f"\n5. Example: Creating Sign Language Video from Text...")
    example_text = ["HELLO", "I", "LOVE", "YOU"]

    print(f"   Input glosses: {example_text}")
    print(f"   Processing each gloss...")

    videos_found = 0
    for gloss in example_text:
        if mapper.gloss_exists(gloss):
            best_video = mapper.get_best_video(gloss)
            print(f"   ✓ '{gloss}' -> video_id: {best_video['video_id']}, source: {best_video['source']}")
            videos_found += 1
        else:
            print(f"   ✗ '{gloss}' -> Not found in dataset")

    print(f"\n   Summary: Found {videos_found}/{len(example_text)} videos")
    print(f"   Next step: Composite videos into single output")
    print(f"   Requires: moviepy (install with: pip install moviepy)")

    print(f"\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nNext steps:")
    print("1. Install moviepy: pip install moviepy")
    print("2. Test video compositing")
    print("3. Integrate with Streamlit app")

if __name__ == "__main__":
    try:
        demo_wlasl_integration()
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
