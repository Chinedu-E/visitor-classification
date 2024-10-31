"use client"
import GenProgess from "@/components/GenProgess";
import Links from "@/components/Links";
import Questions from "@/components/Questions";
import UrlInput from "@/components/UrlInput";
import Image from "next/image";
import { Provider } from 'react-redux'
import { store } from '@/store/store'

export default function Home() {
  return (
    <Provider store={store}>
    <div className="items-center p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] mx-auto max-w-screen-2xl mt-12">
      <main className="flex flex-col gap-8 items-center sm:items-start">
        <UrlInput />
        <Links />
        <GenProgess />
        <Questions />
      </main>
    </div>
    </Provider>
  );
}
