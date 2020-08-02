/** @jsx jsx */
import { jsx } from "@emotion/core";
import React, { useState, useEffect } from "react";
import { Chart } from "./Chart";
import { getCommands, Command, Comment, getCommandComments, Mood } from "./api";
import {
  Card,
  CardHeader,
  Avatar,
  Grid,
  Container,
  Typography,
  CardActionArea,
  useTheme,
  IconButton,
} from "@material-ui/core";
import { red } from "@material-ui/core/colors";
import { CommentInput } from "./CommentInput";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

const App: React.FC = () => {
  const [currentComand, setCurrentCommand] = useState<string>();
  const [commands, setCommands] = useState<Command[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);

  const theme = useTheme();

  async function loadCommands() {
    // TODO: create api
    // const data = await getCommands();
    // setCommands(data);
    setCommands([
      {
        command: "iOS Platform",
        positive: 30,
        negative: 90,
      },
      {
        command: "Global Navigation",
        positive: 30,
        negative: 90,
      },
      {
        command: "DDA Profile",
        positive: 30,
        negative: 90,
      },
      {
        command: "PFM",
        positive: 30,
        negative: 90,
      },
      {
        command: "Госуслуги",
        positive: 30,
        negative: 90,
      },
      {
        command: "DBP.Витрины продаж",
        positive: 30,
        negative: 90,
      },
    ]);
  }

  useEffect(() => {
    loadCommands();
  }, []);

  useEffect(() => {
    async function loadComments() {
      // TODO: create api
      // if (currentComand) {
      //   const data = await getCommandComments(currentComand);
      //   setComments(data);
      // } else {
      //   setComments([]);
      // }

      if (currentComand) {
        setComments([
          {
            text: "Здесь должен быть реальный комментарий пользователя",
            mood: Mood.Positive,
          },
          {
            text: "Здесь должен быть реальный комментарий пользователя",
            mood: Mood.Negative,
          },
          {
            text: "Здесь должен быть реальный комментарий пользователя",
            mood: Mood.Positive,
          },
        ]);
      } else {
        setComments([]);
      }
    }
    loadComments();
  }, [currentComand]);

  return (
    <Container fixed>
      <CommentInput onCommentAdded={loadCommands}></CommentInput>
      {!currentComand && (
        <Typography
          css={{
            marginTop: theme.spacing(8),
          }}
          gutterBottom
          variant="h4"
        >
          Статистика для всех команд
        </Typography>
      )}
      {!currentComand && (
        <div
          css={{
            display: "flex",
            justifyContent: "space-around",
          }}
        >
          <div
            css={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Typography variant="h6">Google Play</Typography>
            <Chart platform="google"></Chart>
          </div>
          <div
            css={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Typography variant="h6">App Store</Typography>
            <Chart platform="ios"></Chart>
          </div>
        </div>
      )}
      {currentComand ? (
        <React.Fragment>
          <div
            css={{
              display: "flex",
              alignItems: "center",
              marginBottom: theme.spacing(3),
            }}
          >
            <IconButton
              onClick={() => setCurrentCommand(undefined)}
              css={{
                marginRight: theme.spacing(3),
              }}
            >
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h4">
              {`Комментарии команды ${currentComand}`}
            </Typography>
          </div>
          <Grid container spacing={3}>
            {comments?.map((comment) => (
              <Grid item xs={12}>
                <Card>
                  <CardHeader
                    title={comment.text}
                    subheader={
                      comment.mood === Mood.Positive
                        ? "Позитивный"
                        : "Негативный"
                    }
                  />
                </Card>
              </Grid>
            ))}
          </Grid>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <Typography gutterBottom variant="h4">
            Команды
          </Typography>
          <Grid container spacing={1}>
            {commands?.map((command) => (
              <Grid item xs={4}>
                <Card>
                  <CardActionArea
                    onClick={() => setCurrentCommand(command.command)}
                  >
                    <CardHeader
                      avatar={
                        <Avatar
                          aria-label="recipe"
                          css={{ backgroundColor: "#ffa726" }}
                        >
                          {command.command.slice(0, 1).toUpperCase()}
                        </Avatar>
                      }
                      title={command.command}
                      subheader={`Позитивных ${command.positive} Негативных ${command.negative}`}
                    />
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        </React.Fragment>
      )}
    </Container>
  );
};

export default App;
