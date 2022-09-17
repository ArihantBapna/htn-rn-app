import {Heading, NativeBaseProvider, Box, Center} from "native-base";

export function TranscriptPage(){
    return (
        <NativeBaseProvider>
            <Box height={"100%"} px={8} safeArea>
                <Heading textAlign={"center"}></Heading>

                <Center my={4}>

                </Center>
            </Box>
        </NativeBaseProvider>
    );
}
