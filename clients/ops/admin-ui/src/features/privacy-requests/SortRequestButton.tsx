import { Flex, Icon, IconButton } from "@fidesui/react";
import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  clearSortFields,
  selectPrivacyRequestFilters,
  setSortDirection,
  setSortField,
} from "./privacy-requests.slice";

type UseSortRequestButtonParams = {
  sortField: string;
  isLoading: boolean;
};

export enum ButtonState {
  ASC = "asc",
  DESC = "desc",
  UNSELECTED = "unselected",
}

const useSortRequestButton = ({
  sortField,
  isLoading,
}: UseSortRequestButtonParams) => {
  const filters = useSelector(selectPrivacyRequestFilters);
  const dispatch = useDispatch();
  const [buttonState, setButtonState] = useState<ButtonState>(
    ButtonState.UNSELECTED
  );
  const [wasButtonJustClicked, setWasButtonJustClicked] = useState(false);
  useEffect(() => {
    if (!isLoading) {
      setWasButtonJustClicked(false);
    }
  }, [isLoading]);

  useEffect(() => {
    if (filters.sort_direction === undefined) {
      setButtonState(ButtonState.UNSELECTED);
    }
  }, [filters]);

  const handleButtonClick = useCallback(() => {
    setWasButtonJustClicked(true);
    dispatch(setSortField(sortField));
    if (buttonState === ButtonState.UNSELECTED) {
      dispatch(setSortDirection(ButtonState.ASC));
      setButtonState(ButtonState.ASC);
    }

    if (buttonState === ButtonState.ASC) {
      dispatch(setSortDirection(ButtonState.DESC));
      setButtonState(ButtonState.DESC);
    }

    if (buttonState === ButtonState.DESC) {
      dispatch(clearSortFields());
      setButtonState(ButtonState.UNSELECTED);
    }
  }, [buttonState, setButtonState, dispatch, sortField]);

  return {
    handleButtonClick,
    buttonState,
    wasButtonJustClicked,
  };
};

type ArrowIconProps = {
  up?: boolean;
};

const ArrowIcon: React.FC<ArrowIconProps> = ({ up }) => {
  if (up === undefined) {
    return (
      <Icon width="24px" height="26px" viewBox="0 0 24 26" fill="none">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="26"
          viewBox="0 0 24 26"
          fill="none"
        >
          <path
            d="M8.72726 15.129L10.9716 12.8145L12 13.875L7.99998 18L4 13.875L5.02837 12.8145L7.27271 15.129V6H8.72726V15.129Z"
            fill="#2D3748"
          />
          <path
            d="M16.7523 8.871V18H15.3089V8.871L13.0205 11.25L12 10.1895L16.0306 6L20 10.125L18.9795 11.1855L16.7523 8.871Z"
            fill="#2D3748"
          />
        </svg>
      </Icon>
    );
  }

  if (up) {
    return (
      <Icon
        width="24px"
        height="26px"
        viewBox="0 0 24 26"
        fill="none"
        style={{
          transform: "rotate(180deg)",
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="26"
          viewBox="0 0 24 26"
          fill="none"
        >
          <g filter="url(#filter0_d_3399_48680)">
            <path
              d="M8.72726 15.129L10.9716 12.8145L12 13.875L7.99998 18L4 13.875L5.02837 12.8145L7.27271 15.129V6H8.72726V15.129Z"
              fill="#2D3748"
            />
            <path
              d="M8.22726 15.129V16.3629L9.08621 15.4771L10.9716 13.5327L11.3035 13.875L7.99998 17.2818L4.69648 13.875L5.02837 13.5327L6.91375 15.4771L7.77271 16.3629V15.129V6.5H8.22726V15.129Z"
              stroke="black"
            />
          </g>
          <path
            d="M16.7523 8.871V18H15.3089V8.871L13.0205 11.25L12 10.1895L16.0306 6L20 10.125L18.9795 11.1855L16.7523 8.871Z"
            fill="#2D3748"
          />
          <defs>
            <filter
              id="filter0_d_3399_48680"
              x="0"
              y="6"
              width="16"
              height="20"
              filterUnits="userSpaceOnUse"
              colorInterpolationFilters="sRGB"
            >
              <feFlood floodOpacity="0" result="BackgroundImageFix" />
              <feColorMatrix
                in="SourceAlpha"
                type="matrix"
                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                result="hardAlpha"
              />
              <feOffset dy="4" />
              <feGaussianBlur stdDeviation="2" />
              <feComposite in2="hardAlpha" operator="out" />
              <feColorMatrix
                type="matrix"
                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"
              />
              <feBlend
                mode="normal"
                in2="BackgroundImageFix"
                result="effect1_dropShadow_3399_48680"
              />
              <feBlend
                mode="normal"
                in="SourceGraphic"
                in2="effect1_dropShadow_3399_48680"
                result="shape"
              />
            </filter>
          </defs>
        </svg>
      </Icon>
    );
  }

  return (
    <Icon width="24px" height="26px" viewBox="0 0 24 26" fill="none">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="26"
        viewBox="0 0 24 26"
        fill="none"
      >
        <g filter="url(#filter0_d_3399_48680)">
          <path
            d="M8.72726 15.129L10.9716 12.8145L12 13.875L7.99998 18L4 13.875L5.02837 12.8145L7.27271 15.129V6H8.72726V15.129Z"
            fill="#2D3748"
          />
          <path
            d="M8.22726 15.129V16.3629L9.08621 15.4771L10.9716 13.5327L11.3035 13.875L7.99998 17.2818L4.69648 13.875L5.02837 13.5327L6.91375 15.4771L7.77271 16.3629V15.129V6.5H8.22726V15.129Z"
            stroke="black"
          />
        </g>
        <path
          d="M16.7523 8.871V18H15.3089V8.871L13.0205 11.25L12 10.1895L16.0306 6L20 10.125L18.9795 11.1855L16.7523 8.871Z"
          fill="#2D3748"
        />
        <defs>
          <filter
            id="filter0_d_3399_48680"
            x="0"
            y="6"
            width="16"
            height="20"
            filterUnits="userSpaceOnUse"
            colorInterpolationFilters="sRGB"
          >
            <feFlood floodOpacity="0" result="BackgroundImageFix" />
            <feColorMatrix
              in="SourceAlpha"
              type="matrix"
              values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
              result="hardAlpha"
            />
            <feOffset dy="4" />
            <feGaussianBlur stdDeviation="2" />
            <feComposite in2="hardAlpha" operator="out" />
            <feColorMatrix
              type="matrix"
              values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"
            />
            <feBlend
              mode="normal"
              in2="BackgroundImageFix"
              result="effect1_dropShadow_3399_48680"
            />
            <feBlend
              mode="normal"
              in="SourceGraphic"
              in2="effect1_dropShadow_3399_48680"
              result="shape"
            />
          </filter>
        </defs>
      </svg>
    </Icon>
  );
};

type SortRequestButtonProps = {
  sortField: string;
  isLoading: boolean;
};

const SortRequestButton: React.FC<SortRequestButtonProps> = ({
  sortField,
  isLoading,
}) => {
  const { buttonState, handleButtonClick, wasButtonJustClicked } =
    useSortRequestButton({ sortField, isLoading });

  let icon = null;

  switch (buttonState) {
    case ButtonState.ASC:
      icon = <ArrowIcon up />;
      break;
    case ButtonState.DESC:
      icon = <ArrowIcon up={false} />;
      break;
    case ButtonState.UNSELECTED:
      icon = <ArrowIcon />;
      break;
    default:
      icon = <ArrowIcon />;
  }

  return (
    <Flex paddingLeft="3px">
      <IconButton
        variant="ghost"
        aria-label="Sort requests"
        icon={icon}
        isLoading={isLoading && wasButtonJustClicked}
        onClick={handleButtonClick}
      />
    </Flex>
  );
};

export default SortRequestButton;
