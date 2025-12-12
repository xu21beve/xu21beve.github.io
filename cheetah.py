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

from pvcheetah import CheetahActivationLimitError, create
from pvrecorder import PvRecorder
import pvkoala
import wave

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
spotlit = True # is only true for the robot that is currently hanging
disabledRobot = False
damagedRobot = False
onstage = False
harmony = False
justDid = 0 # 0 - nothing, 1 - speaker attempted, 2 - amp attempted, 3 - pickup attempted

keywordKey = [[nonfunctionalRobot, "functional robot"], [damagedRobot, "damaged"], [disabledRobot, "disabled"], [defenseRobot, "defense"], [harmony, "harmony"], [spotlit, "spotlit"], [amplified, "amplified"], [onstage, "onstage"], [blockedOpponentRobot, "blocked"], [trapScored, "trap"], [highNotes, "high note"], [teleopSpeakerShots, "teleop speaker"], [autoSpeakerShots, "auton speaker"], [teleopAmpShots, "teleop amping"], [autoAmpShots, "auton amping"], [notesDropped, "drop"], [pickUps, "pickup"]]
def Update(search_string):
	for i, tup in enumerate(keywordKey):
		if "autonomous" in search_string.lower() or inAutonomous:
			inAutonomous = True
			if "pickup" in search_string.lower():
				pickUps += 1
				justDid = 3
			if "speaker" in search_string.lower():
				autonSpeakerShots += 1
				justDid = 1
			if "amp" in search_string.lower():
				autonAmpShots += 1
				justDid = 2
			if "drop" in search_string.lower():
				if justDid == 0:
					return
				elif justDid == 1:
					autonSpeakerShots -= 1
				elif justDid == 2:
					autonAmpShots -= 1
				notesDropped += 1					
		elif "driver" in search_string.lower(): 
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
				elif justDid == 2:
					teleopAmpShots -= 1
				notesDropped += 1
			if "onstage" in search_string.lower():
				onstage = True
			if "trap" in search_string.lower():
				trapScored = True
			if "defense" in search_string.lower():
				defenseRobot = True
			if "disabled" in search_string.lower():
				disabledRobot = True
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

def read_wav_file(file_path):
    with wave.open(file_path, 'rb') as wf:
        rate = wf.getframerate()
        audio_data = wf.readframes(wf.getnframes())
        return audio_data, rate

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
        '--endpoint_duration_sec',
        type=float,
        default=1.,
        help='Duration in seconds for speechless audio to be considered an endpoint')
    parser.add_argument(
        '--disable_automatic_punctuation',
        action='store_true',
        help='Disable insertion of automatic punctuation')
    parser.add_argument(
        '--input_file',
        help='Absolute path to input file')
    parser.add_argument('--audio_device_index', type=int, default=-1, help='Index of input audio device')
    parser.add_argument('--show_audio_devices', action='store_true', help='Only list available devices and exit')
    args = parser.parse_args()

    if args.show_audio_devices:
        for index, name in enumerate(PvRecorder.get_available_devices()):
            print('Device #%d: %s' % (index, name))
        return

    if not args.access_key:
        print('--access_key is required.')
        return

    cheetah = create(
        access_key=args.access_key,
        library_path=args.library_path,
        model_path=args.model_path,
        endpoint_duration_sec=args.endpoint_duration_sec,
        enable_automatic_punctuation=not args.disable_automatic_punctuation)
    koala = pvkoala.create(access_key=args.access_key)


    try:
        print('Cheetah version : %s' % cheetah.version)

        recorder = PvRecorder(frame_length=cheetah.frame_length, device_index=args.audio_device_index)
        recorder.start()
        print('Listening... (press Ctrl+C to stop)')

        try:
            while True:
                # partial_transcript, is_endpoint = cheetah.process(recorder.read())
                partial_transcript, is_endpoint = cheetah.process(read_wav_file(args.input_file))
                print(partial_transcript, end='', flush=True)
                if is_endpoint:
                    print(cheetah.flush())
                    if keywordKey[7][0]:
                        print(keywordKey)
                        break
        finally:
            print()
            recorder.stop()

    except KeyboardInterrupt:
        pass
    except CheetahActivationLimitError:
        print('AccessKey has reached its processing limit.')
    finally:
        cheetah.delete()


if __name__ == '__main__':
    main()
    for tup in keywordKey:
        print(tup[1] + str(tup[0]))
	

# import time
# start_time = time.time()
# # Your code here
# end_time = time.time()
# elapsed_time = end_time - start_time