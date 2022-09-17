import {Text, View} from "react-native";

export const SqView = View as any;
export const SqText = Text as any;

export function HomePage(){
    return (
        <SqView className="flex-1 items-center justify-center bg-white">
            <SqText className={"text-red-700"}>Home Screen</SqText>
        </SqView>
    );
}
