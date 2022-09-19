import React, { useState } from "react";
import { Box, Button } from "@fidesui/react";
import { router } from "next/client";
import RequestModal from "../RequestModal";

import type { AlertState } from "../../../types/AlertState";

import config from "../../../config/config.json";

import { ModalViews } from "../types";
import ConsentRequestForm from "./ConsentRequestForm";

export const useConsentRequestModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [openAction, setOpenAction] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<ModalViews>(
    ModalViews.ConsentRequest
  );
  const [consentRequestId, setConsentRequestId] = useState<string>("");

  const onOpen = (action: string) => {
    setCurrentView(ModalViews.ConsentRequest);
    setOpenAction(action);
    setIsOpen(true);
  };

  const onClose = () => {
    setIsOpen(false);
    setOpenAction(null);
    setCurrentView(ModalViews.ConsentRequest);
    setConsentRequestId("");
  };

  return {
    isOpen,
    onClose,
    onOpen,
    openAction,
    currentView,
    setCurrentView,
    consentRequestId,
    setConsentRequestId,
  };
};

export type ConsentRequestModalProps = {
  isOpen: boolean;
  onClose: () => void;
  openAction: string | null;
  setAlert: (state: AlertState) => void;
  currentView: ModalViews;
  setCurrentView: (view: ModalViews) => void;
  consentRequestId: string;
  setConsentRequestId: (id: string) => void;
  isVerificationRequired: boolean;
};

export const ConsentRequestModal: React.FC<ConsentRequestModalProps> = ({
  isOpen,
  onClose,
  openAction,
  setAlert,
  currentView,
  setCurrentView,
  consentRequestId,
  setConsentRequestId,
  isVerificationRequired,
}) => {
  const action = openAction
    ? config.actions.filter(({ policy_key }) => policy_key === openAction)[0]
    : null;

  if (!action) return null;

  let form = null;

  if (currentView === ModalViews.ConsentRequest) {
    form = (
      <ConsentRequestForm
        isOpen={isOpen}
        onClose={onClose}
        openAction={openAction}
        setAlert={setAlert}
        setCurrentView={setCurrentView}
        setPrivacyRequestId={setConsentRequestId}
        isVerificationRequired={isVerificationRequired}
      />
    );
  }

  if (currentView === ModalViews.IdentityVerification) {
    form = (
      <Box>
        PLACEHOLDER VERIFICATION VIEW. Actual verification will be added once
        the apis are finished.
        <Button
          onClick={() => {
            onClose();
            router.push("/consent");
          }}
        >
          Go to consent page
        </Button>
      </Box>
    );
  }

  return (
    <RequestModal isOpen={isOpen} onClose={onClose}>
      {form}
    </RequestModal>
  );
};
