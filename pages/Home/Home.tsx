import { signOut } from "@firebase/auth";
import {Button, Box, Fab, Text, useToast} from "native-base";
import {auth, db} from "../../firebase";
import { Audio } from 'expo-av';
import {useState} from "react";
import {Recording} from "expo-av/build/Audio/Recording";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { doc, setDoc } from "firebase/firestore";

export function HomePage() {
  const toast = useToast();
  const [recording, setRecording] = useState<Recording>();

  async function startRecording(){
    try{
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync(
          Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      setRecording(recording);
    } catch (err) {
        console.error('Failed to start recording', err);
    }
  }

  function callTheApi(fileName: string, fileUrl: string, userId: string){
    // Do shit with the file data

  }

  async function stopRecording(){
    await recording?.stopAndUnloadAsync();
    const uri = recording?.getURI();
    setRecording(undefined);
    if (uri){
      await fetch(uri).then(r => {
        r.blob().then(blob => {
          const storage = getStorage();
          const time = new Date().getMilliseconds().toString();
          const storageRef = ref(storage, `${auth.currentUser?.uid}/${time}.${blob.type.split("/")[1]}`);
          uploadBytes(storageRef, blob).then((snapshot) => {
            getDownloadURL(snapshot.ref).then(async url => {
              await setDoc(doc(db, "audio-transcripts", `${auth.currentUser?.uid}-${time}.${blob.type.split("/")[1]}`), {
                audiofile: `${auth.currentUser?.uid}-${time}.${blob.type.split("/")[1]}`,
                flashcards: '[]',
                url: url,
                userid: auth.currentUser?.uid,
              }).then(() => {
                toast.show({title: "Uploaded Audio file successfully", backgroundColor: "green.500"});
                let fileName = `${auth.currentUser?.uid}-${time}.${blob.type.split("/")[1]}`;
                let fileUrl = url;
                let userId = auth.currentUser?.uid || "";
                callTheApi(fileName, fileUrl, userId);
              }).catch(err => {
                toast.show({title: "Error setting data", backgroundColor: "red.500"});
              })
            }).catch(err => {
              toast.show({title: "Error getting download url", backgroundColor: "red.500"});
            })


          }).catch((e) => {
            toast.show({title: "Error uploading audio file", backgroundColor: "red.500"});
          });
        });
      });
    }
  }

  return (
    <Box height={"100%"} safeArea>
      <Text>This is Home Page</Text>

      <Button
          onPress={() => {
            signOut(auth)
                .then()
                .catch((error) => {
                  toast.show({
                    title: error.code,
                    description: error.message,
                    backgroundColor: "red.600",
                  });
                });
          }}
      >
        Logout
      </Button>
      <Fab onPress={recording ? stopRecording : startRecording } renderInPortal={false} shadow={2} size="lg"/>
    </Box>
  );
}
