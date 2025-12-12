#
#    Copyright 2018-2023 Picovoice Inc.
#
#    You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
#    file accompanying this source.
#
#    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#    an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#    specific language governing permissions and limitations under the License.
#

import argparse
import struct
import wave

from pvcheetah import CheetahActivationLimitError, create

# Initialize the scoring 
inAutonomous = False
inTeleop = False
teleopSpeakerShots = 0
autoSpeakerShots = 0
teleopAmpShots = 0
autoAmpShots = 0
notesDropped = 0
pickUps = 0
nonfunctionalRobot = False
highNotes = 0
trapScored = False
blockedOpponentRobot = 0 # counts how many times the robot blocks another robot
amplified = 0 # counts how many times amplified
defenseRobot = False
spotlit = False # is only true for the robot that is currently hanging
disabledRobot = False
damagedRobot = False
onstage = False
harmony = False
justDid = 0 # 0 - nothing, 1 - speaker attempted, 2 - amp attempted, 3 - pickup attempted

keywordKey = [
    [inAutonomous, "functional robot"], 
    [damagedRobot, "damaged"], 
    [disabledRobot, "disabled"], 
    [defenseRobot, "defense"], 
    [harmony, "harmony"], 
    [spotlit, "spotlit"], 
    [amplified, "amplified"], 
    [onstage, "onstage"], 
    [blockedOpponentRobot, "blocked"], 
    [trapScored, "trap"], 
    [highNotes, "high note"], 
    [teleopSpeakerShots, "teleop speaker"], 
    [autoSpeakerShots, "auton speaker"], 
    [teleopAmpShots, "teleop amping"], 
    [autoAmpShots, "auton amping"], 
    [notesDropped, "drop"], 
    [pickUps, "pickup"]
]

def Update(search_string):
	global inAutonomous, inTeleop, teleopSpeakerShots, autoSpeakerShots, teleopAmpShots, autoAmpShots, notesDropped, pickUps, nonfunctionalRobot, highNotes, trapScored, blockedOpponentRobot, amplified, defenseRobot, spotlit, disabledRobot, damagedRobot, onstage, harmony, justDid
	if "autonomous" in search_string.lower() or inAutonomous:
		inAutonomous = True
		if "pickup" in search_string.lower():
			pickUps += 1
			justDid = 3
		if "speaker" in search_string.lower():
			autoSpeakerShots += 1
			justDid = 1
		if "amp" in search_string.lower():
			autoAmpShots += 1
			justDid = 2
		if "drop" in search_string.lower():
			if justDid == 0:
				return
			elif justDid == 1:
				autoSpeakerShots -= 1
			elif justDid == 2:
				autoAmpShots -= 1
			notesDropped += 1					
	if "operator" in search_string.lower() or inTeleop: 
		inAutonomous = False
		inTeleop = True
		if "pickup" in search_string.lower():
			pickUps += 1
			justDid = 3
		if "speaker" in search_string.lower():
			teleopSpeakerShots += 1
			justDid = 1
		if "amp" in search_string.lower():
			teleopAmpShots += 1
			justDid = 2
		if "drop" in search_string.lower():
			if justDid == 0:
				return
			elif justDid == 1:
				teleopSpeakerShots -= 1
				notesDropped += 1
			elif justDid == 2:
				teleopAmpShots -= 1
				notesDropped += 1
		if "onstage" in search_string.lower():
			onstage = True
		if "trap" in search_string.lower():
			trapScored = True
		if "defense" in search_string.lower():
			defenseRobot = True
		if "harmony" in search_string.lower():
			harmony = True
		if "spotlit" in search_string.lower():
			spotlit = True
		if "amplified" in search_string.lower():
			amplified += 1
		if "blocked" in search_string.lower():
			blockedOpponentRobot += 1
		if "high" in search_string.lower():
			highNotes += 1
	if "disabled" in search_string.lower():
		disabledRobot = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--access_key',
        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')
    parser.add_argument(
        '--library_path',
        help='Absolute path to dynamic library. Default: using the library provided by `pvcheetah`')
    parser.add_argument(
        '--model_path',
        help='Absolute path to Cheetah model. Default: using the model provided by `pvcheetah`')
    parser.add_argument(
        '--disable_automatic_punctuation',
        action='store_true',
        help='Disable insertion of automatic punctuation')
    parser.add_argument(
        '--wav_paths',
        nargs='+',
        required=True,
        metavar='PATH',
        help='Absolute paths to `.wav` files to be transcribed')
    args = parser.parse_args()

    o = create(
        access_key=args.access_key,
        model_path=args.model_path,
        library_path=args.library_path,
        enable_automatic_punctuation=not args.disable_automatic_punctuation)

    try:
        for wav_path in args.wav_paths:
            with wave.open(wav_path, 'rb') as f:
                if f.getframerate() != o.sample_rate:
                    raise ValueError(
                        "invalid sample rate of `%d`. cheetah only accepts `%d`" % (f.getframerate(), o.sample_rate))
                if f.getnchannels() != 1:
                    raise ValueError("this demo can only process single-channel WAV files")
                if f.getsampwidth() != 2:
                    raise ValueError("this demo can only process 16-bit WAV files")

                buffer = f.readframes(f.getnframes())
                audio = struct.unpack('%dh' % (len(buffer) / struct.calcsize('h')), buffer)

            num_frames = len(audio) // o.frame_length
            transcript = ''
            Update("autonomous")
            for i in range(num_frames):
                if i == 8:
                    Update("speaker")
                    Update("Operator")
                frame = audio[i * o.frame_length:(i + 1) * o.frame_length]
                partial_transcript, _ = o.process(frame)
                Update(partial_transcript)
                print(partial_transcript, end='', flush=True)
                transcript += partial_transcript

                if keywordKey[7][0]:
                    print(keywordKey)
                    break

            final_transcript = o.flush()
            print(final_transcript)

    except CheetahActivationLimitError:
        print('AccessKey has reached its processing limit.')
    finally:
        o.delete()


if __name__ == '__main__':
	main()
	print("inAutonomous:", inAutonomous)
	print("inTeleop:", inTeleop)
	print("teleopSpeakerShots:", teleopSpeakerShots)
	print("autoSpeakerShots:", autoSpeakerShots)
	print("teleopAmpShots:", teleopAmpShots)
	print("autoAmpShots:", autoAmpShots)
	print("notesDropped:", notesDropped)
	print("pickUps:", pickUps)
	print("nonfunctionalRobot:", nonfunctionalRobot)
	print("highNotes:", highNotes)
	print("trapScored:", trapScored)
	print("blockedOpponentRobot:", blockedOpponentRobot)
	print("amplified:", amplified)
	print("defenseRobot:", defenseRobot)
	print("spotlit:", spotlit)
	print("disabledRobot:", disabledRobot)
	print("damagedRobot:", damagedRobot)
	print("onstage:", onstage)
	print("harmony:", harmony)