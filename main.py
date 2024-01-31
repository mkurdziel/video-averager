import cv2
import numpy as np
import sys

def process_video(input_file, output_file, n_frames):
    # Open the input video
    cap = cv2.VideoCapture(input_file)

    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object to save the output video
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Initialize a list to hold the frames for running average calculation
    frame_queue = []
    frame_sum = None

    while True:
        ret, frame = cap.read()

        if not ret:
            break  # Exit the loop if no more frames are available

        if frame_sum is None:
            # Initialize the frame sum array with the same shape and type as the first frame
            frame_sum = np.zeros_like(frame, dtype=np.float32)

        # Convert frame to float for accurate summation and averaging
        float_frame = np.float32(frame)

        # Add the current frame to the sum and to the queue
        frame_sum += float_frame
        frame_queue.append(float_frame)

        if len(frame_queue) > n_frames:
            # Subtract the oldest frame from the sum and remove it from the queue
            frame_sum -= frame_queue.pop(0)

        # Calculate the running average
        avg_frame = frame_sum / min(len(frame_queue), n_frames)

        # Convert the averaged frame back to uint8 for video writing
        avg_frame_uint8 = np.uint8(avg_frame)

        # Write the averaged frame to the output video
        out.write(avg_frame_uint8)

    # Release everything if the job is finished
    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_file> <n_frames>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    n_frames = int(sys.argv[3])

    process_video(input_file, output_file, n_frames)
