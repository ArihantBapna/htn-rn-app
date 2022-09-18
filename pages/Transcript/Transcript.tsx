import {
  Heading,
  NativeBaseProvider,
  Box,

  Center,
  ScrollView,
  useToast,
} from "native-base";
import { useEffect, useState } from "react";
import axios from "axios";
// @ts-ignore
import image from "./assets/bg.png";
import {ImageBackground, View} from "react-native";

export function TranscriptPage({ route, navigation }: any) {
  const { recording } = route.params;
  // const baseUrl = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:8080' : "https://src-usbebnquka-ue.a.run.app";
  const baseUrl = "http://127.0.0.1:8080";
  const [transcript, setTranscript] = useState<any>();
  const toast = useToast();

  useEffect(() => {
    axios
      .post("https://src-usbebnquka-ue.a.run.app/get_prof_transcript", {
        url: recording.url,
      })
      .then((res) => {
        console.log(res.data);
        setTranscript(res.data);
      })
      .catch((err) => {
        console.log(err);
        toast.show({title: "Error", description: "There was an error getting the transcript. Please try again.", backgroundColor: "red.500"})
      });
    // axios.get('http://127.0.0.1:8080/get_transcript_url', {
    //     data: {
    //         url: recording
    //     }
    // }).then((res) => {
    //    console.log(res);
    // }).catch(err => {
    //     console.log(err);
    // });
  });

  return (
    <NativeBaseProvider>
      <ImageBackground resizeMode='cover'  source={image} style={{width: "100%", height: "100%"}}>
        <View style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center"
        }}>
          <Box height={"100%"} px={8} pt={8} safeArea>
            <Center>
              {!transcript ? (
                <Heading>Transcript is loading...</Heading>
              ) : (
                <>
                  <Heading>Your Transcript</Heading>
                  <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center' }}>
                    {transcript['speaker_lst'].map((speaker : any, index : number) => {
                      return (
                          <Box key={index}>
                            <Heading>{speaker}:</Heading>
                            <Heading>{transcript[speaker]}</Heading>
                          </Box>
                      );
                    })}
                  </ScrollView>
                </>
              )}
            </Center>
          </Box>
        </View>
      </ImageBackground>
    </NativeBaseProvider>
  );
}
