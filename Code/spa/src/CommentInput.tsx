/** @jsx jsx */
import { jsx } from "@emotion/core";
import React, { useState } from "react";
import {
  Paper,
  IconButton,
  InputBase,
  useTheme,
  Snackbar,
} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import { getCommentCommandAndMood, CommentCommand, Mood } from "./api";
import MuiAlert, { AlertProps } from "@material-ui/lab/Alert";

function Alert(props: AlertProps) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

interface Props {
  onCommentAdded: () => void;
}

export const CommentInput: React.FC<Props> = ({ onCommentAdded }) => {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [commentInfo, setCommentInfo] = useState<CommentCommand>();
  const theme = useTheme();

  const handleAddComment = async () => {
    // TODO: create api
    const data = await getCommentCommandAndMood(value);
    setCommentInfo(data);
    setOpen(true);
    onCommentAdded();

    // setCommentInfo({
    //   command: "DBP.Витрины продаж",
    //   mood: Mood.Positive,
    // });
    // setOpen(true);
    // onCommentAdded();
  };

  const handleClose = (event?: React.SyntheticEvent, reason?: string) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
  };

  return (
    <Paper
      component="form"
      css={{
        marginTop: theme.spacing(8),
        padding: "2px 4px",
        display: "flex",
        alignItems: "center",
        width: "100%",
      }}
    >
      <InputBase
        multiline
        rows={3}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        css={{ marginLeft: theme.spacing(1), flex: 1 }}
        placeholder="Введите комментарий"
      />
      <IconButton
        onClick={handleAddComment}
        color="primary"
        css={{
          padding: 10,
        }}
      >
        <AddIcon />
      </IconButton>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={open}
        autoHideDuration={15000}
        onClose={handleClose}
      >
        <Alert
          onClose={handleClose}
          severity={commentInfo?.mood === Mood.Positive ? "success" : "error"}
        >
          {commentInfo?.mood === Mood.Positive
            ? `Позитивный комментарий адресованный команде ${commentInfo?.command}`
            : `Негативный комментарий адресованный команде ${commentInfo?.command}`}
        </Alert>
      </Snackbar>
    </Paper>
  );
};
