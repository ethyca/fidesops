import React, { useState } from "react";
import { Modal, ModalOverlay, ModalContent } from "@fidesui/react";

import type { AlertState } from "../../types/AlertState";

import config from "../../config/config.json";

import { PrivacyRequestForm } from "./PrivacyRequestForm";

export const useRequestModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [openAction, setOpenAction] = useState<string | null>(null);

  const onOpen = (action: string) => {
    setOpenAction(action);
    setIsOpen(true);
  };

  const onClose = () => {
    setIsOpen(false);
    setOpenAction(null);
  };

  return { isOpen, onClose, onOpen, openAction };
};

export const RequestModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  openAction: string | null;
  setAlert: (state: AlertState) => void;
}> = ({ isOpen, onClose, openAction, setAlert }) => {
  const action = openAction
    ? config.actions.filter(({ policy_key }) => policy_key === openAction)[0]
    : null;

  if (!action) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent top={[0, "205px"]} maxWidth="464px" mx={5} my={3}>
        <PrivacyRequestForm
          isOpen={isOpen}
          onClose={onClose}
          openAction={openAction}
          setAlert={setAlert}
        />
      </ModalContent>
    </Modal>
  );
};
