import {useColorScheme} from "nativewind";
import {SqView, SqText, SqPressable, SqSafeAreaView} from "../../NativewindComponents";


export function HomePage(){
    const { colorScheme, toggleColorScheme } = useColorScheme();

    return (
        <SqSafeAreaView className={"h-full"}>
            <SqView className="flex-1 items-center justify-center bg-white dark:bg-slate-800 dark:text-white">
                <SqText  className={"dark:text-white"}>Home Screen</SqText>
                <SqPressable
                    onPress={toggleColorScheme}
                    className="flex-1 items-center justify-center"
                >
                    <SqText
                        selectable={false}
                        className={"dark:text-white"}
                    >
                        {`Try clicking me! ${colorScheme === "dark" ? "🌙" : "🌞"}`}
                    </SqText>
                </SqPressable>
            </SqView>
        </SqSafeAreaView>
    );
}
