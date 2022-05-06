import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    Textarea,
    Button,
} from "@fidesui/react";
import React from 'react';



type DenyModalProps ={
    isOpen: boolean
    handleMenuClose:  () => void
    denialReason: string
    onChange: ()=> void
}

const DenyModal = ({ isOpen, handleMenuClose, denialReason, onChange}: DenyModalProps ) => (
    <Modal isOpen={isOpen} onClose={handleMenuClose} isCentered>
        <ModalOverlay />
        <ModalContent width='100%' maxWidth='456px'>
            <ModalHeader>Data subject request denial</ModalHeader>
            <ModalBody color="gray.500" fontSize='14px'>
                Please enter a reason for denying this data subject request
            </ModalBody>
            <ModalBody>
                <Textarea focusBorderColor="primary.600" value={denialReason} onChange={onChange}/>
            </ModalBody>
            <ModalFooter>
                <Button
                    size='sm'
                    width='100%'
                    maxWidth='198px'
                    colorScheme='gray.200'
                    mr={3}
                    onClick={handleMenuClose}>
                    Close
                </Button>
                <Button
                    size='sm'
                    width='100%'
                    maxWidth='198px'
                    colorScheme='primary'
                    variant='solid'
                    onClick={()=>{console.log("denial reason: ", denialReason)}}
                    >
                    Confirm
                </Button>
            </ModalFooter>
        </ModalContent>
    </Modal>
)

export default DenyModal;