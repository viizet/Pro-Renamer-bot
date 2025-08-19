import time
import os
import asyncio
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser



async def fix_thumb(thumb):
    width = 320
    height = 180
    try:
        if thumb != None:
            # Open and convert image
            img = Image.open(thumb).convert("RGB")
            
            # Calculate 16:9 aspect ratio dimensions
            target_width = 320
            target_height = 180
            
            # Get current dimensions
            current_width, current_height = img.size
            
            # Calculate aspect ratios
            current_ratio = current_width / current_height
            target_ratio = target_width / target_height
            
            if current_ratio > target_ratio:
                # Image is wider, crop width to fit 16:9
                new_height = current_height
                new_width = int(current_height * target_ratio)
                left = (current_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, new_height))
            else:
                # Image is taller, crop height to fit 16:9
                new_width = current_width
                new_height = int(current_width / target_ratio)
                top = (current_height - new_height) // 2
                img = img.crop((0, top, new_width, top + new_height))
            
            # Resize to final 16:9 dimensions
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            img.save(thumb, "JPEG", quality=95, optimize=True)
            
    except Exception as e:
        print(f"Error processing thumbnail: {e}")
        thumb = None 
       
    return width, height, thumb
    
async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        "-vf",
        "scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2:black",  # Force 16:9 with black padding
        "-q:v",
        "2",  # High quality but fast encoding
        "-threads",
        "2",  # Use multiple threads
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None



async def convert_to_16_9(input_path, output_path, ms):
    try:
        await ms.edit("<i>Converting to 16:9 aspect ratio ⚡</i>")
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black',
            '-c:a', 'copy',
            '-preset', 'fast',
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)

        if os.path.exists(output_path):
            await ms.edit("<i>Successfully converted to 16:9 aspect ratio ✅</i>")
            return output_path
        else:
            await ms.edit("<i>Failed to convert aspect ratio ❌</i>")
            return None
    except Exception as e:
        print(f"Error occurred while converting aspect ratio: {str(e)}")
        await ms.edit("<i>An Error Occurred While Converting Aspect Ratio ❌</i>")
        return None

async def add_metadata(input_path, output_path, metadata, ms):
    try:
        await ms.edit("<i>I Found Metadata, Adding Into Your File ⚡</i>")
        command = [
            'ffmpeg', '-y', '-i', input_path, '-map', '0', '-c:s', 'copy', '-c:a', 'copy', '-c:v', 'copy',
            '-metadata', f'title={metadata}',  # Set Title Metadata
            '-metadata', f'author={metadata}',  # Set Author Metadata
            '-metadata:s:s', f'title={metadata}',  # Set Subtitle Metadata
            '-metadata:s:a', f'title={metadata}',  # Set Audio Metadata
            '-metadata:s:v', f'title={metadata}',  # Set Video Metadata
            '-metadata', f'artist={metadata}',  # Set Artist Metadata
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)

        
        if os.path.exists(output_path):
            await ms.edit("<i>Metadata Has Been Successfully Added To Your File ✅</i>")
            return output_path
        else:
            await ms.edit("<i>Failed To Add Metadata To Your File ❌</i>")
            return None
    except Exception as e:
        print(f"Error occurred while adding metadata: {str(e)}")
        await ms.edit("<i>An Error Occurred While Adding Metadata To Your File ❌</i>")
        return None

async def add_metadata_with_16_9(input_path, output_path, metadata, ms):
    try:
        await ms.edit("<i>Adding metadata and converting to 16:9 aspect ratio ⚡</i>")
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black',
            '-c:a', 'copy',
            '-preset', 'fast',
            '-metadata', f'title={metadata}',
            '-metadata', f'author={metadata}',
            '-metadata:s:s', f'title={metadata}',
            '-metadata:s:a', f'title={metadata}',
            '-metadata:s:v', f'title={metadata}',
            '-metadata', f'artist={metadata}',
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)

        if os.path.exists(output_path):
            await ms.edit("<i>Successfully added metadata and converted to 16:9 ✅</i>")
            return output_path
        else:
            await ms.edit("<i>Failed to process video ❌</i>")
            return None
    except Exception as e:
        print(f"Error occurred while processing video: {str(e)}")
        await ms.edit("<i>An Error Occurred While Processing Video ❌</i>")
        return None
    






# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Back-Up Channel @JishuBotz
# Developer @JishuDeveloper & @MadflixOfficials
