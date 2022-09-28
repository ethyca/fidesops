import React, { useState } from "react";
import type { NextPage } from "next";
import Head from "next/head";
import { Flex, Heading, Text, Stack, Image, Button } from "@fidesui/react";

import ConsentItem from "../components/ConsentItem";

import config from "../config/config.json";

type UserConsent = {
  data_use: string;
  data_use_description?: string;
  opt_in: boolean;
}

const Consent: NextPage = () => {
  const content: any = [];
  const [ userConsents, setUserConsents] = useState();

  config.consent.consentOptions.forEach((option) => {
    content.push(
      <ConsentItem
        fidesDataUseKey={option.fidesDataUseKey}
        name={option.name}
        description={option.description}
        highlight={option.highlight}
        url={option.url}
        defaultValue={option.default}
      />
    );
  });

  return (
    <div>
      <Head>
        <title>Privacy Center</title>
        <meta name="description" content="Privacy Center" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header>
        <Flex
          bg="gray.100"
          minHeight={14}
          p={1}
          width="100%"
          justifyContent="center"
          alignItems="center"
        >
          <Image
            src={config.logo_path}
            height="56px"
            width="304px"
            alt="Logo"
          />
        </Flex>
      </header>

      <main>
        <Stack align="center" py={["6", "16"]} px={5} spacing={8}>
          <Stack align="center" spacing={3}>
            <Heading
              fontSize={["3xl", "4xl"]}
              color="gray.600"
              fontWeight="semibold"
              textAlign="center"
            >
              Manage your consent
            </Heading>
            <Text
              fontSize={["small", "medium"]}
              fontWeight="medium"
              maxWidth={624}
              textAlign="center"
              color="gray.600"
            >
              When you use our services, you’re trusting us with your
              information. We understand this is a big responsibility and work
              hard to protect your information and put you in control.
            </Text>
          </Stack>
          <Flex m={-2} flexDirection="column">
            {content}
          </Flex>
        </Stack>
        <Button onClick={()=>{console.log()}}>Save</Button>
      </main>
    </div>
  );
};

export default Consent;
